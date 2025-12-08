"""LLM Service for integrating with multiple LLM providers."""

import logging
import os
from abc import ABC, abstractmethod
from typing import Optional

import httpx

logger = logging.getLogger(__name__)


class ConfigurationError(Exception):
    """Raised when LLM service is not properly configured."""
    pass


class RateLimitError(Exception):
    """Raised when API rate limit is exceeded."""
    
    def __init__(self, message: str, retry_after: Optional[int] = None):
        super().__init__(message)
        self.retry_after = retry_after


class AuthenticationError(Exception):
    """Raised when API authentication fails."""
    pass


class TimeoutError(Exception):
    """Raised when API request times out."""
    pass


class LLMAdapter(ABC):
    """Abstract base class for LLM provider adapters."""
    
    @abstractmethod
    async def complete(self, prompt: str, model: Optional[str] = None) -> tuple[str, int, int]:
        """
        Generate completion from prompt.
        
        Args:
            prompt: Input prompt text
            model: Optional model override
            
        Returns:
            Tuple of (response_text, input_tokens, output_tokens)
        """
        pass
    
    @abstractmethod
    def calculate_cost(self, input_tokens: int, output_tokens: int, model: str) -> float:
        """
        Calculate cost for token usage.
        
        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            model: Model name
            
        Returns:
            Cost in USD
        """
        pass
    
    @abstractmethod
    async def close(self) -> None:
        """Close any open connections."""
        pass


class AnthropicAdapter(LLMAdapter):
    """Adapter for Anthropic Claude models."""
    
    # Pricing per million tokens (as of Nov 2024)
    PRICING = {
        "claude-3-5-sonnet-20241022": {"input": 3.0, "output": 15.0},
        "claude-3-5-sonnet-20240620": {"input": 3.0, "output": 15.0},
        "claude-3-opus-20240229": {"input": 15.0, "output": 75.0},
        "claude-3-sonnet-20240229": {"input": 3.0, "output": 15.0},
        "claude-3-haiku-20240307": {"input": 0.25, "output": 1.25},
    }
    
    DEFAULT_MODEL = "claude-3-5-sonnet-20241022"
    
    def __init__(self, api_key: str, timeout: float = 120.0):
        """
        Initialize Anthropic adapter.
        
        Args:
            api_key: Anthropic API key
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None
    
    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=self.timeout,
                headers={
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json"
                }
            )
        return self._client
    
    async def complete(self, prompt: str, model: Optional[str] = None) -> tuple[str, int, int]:
        """Generate completion using Claude."""
        model = model or self.DEFAULT_MODEL
        client = await self._get_client()
        
        try:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                json={
                    "model": model,
                    "max_tokens": 4096,
                    "messages": [{"role": "user", "content": prompt}]
                }
            )
            response.raise_for_status()
            
            data = response.json()
            text = data["content"][0]["text"]
            input_tokens = data["usage"]["input_tokens"]
            output_tokens = data["usage"]["output_tokens"]
            
            return text, input_tokens, output_tokens
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise AuthenticationError("Invalid Anthropic API key")
            elif e.response.status_code == 429:
                retry_after = e.response.headers.get("retry-after")
                raise RateLimitError(
                    "Anthropic API rate limit exceeded",
                    retry_after=int(retry_after) if retry_after else None
                )
            else:
                raise
        except httpx.TimeoutException:
            raise TimeoutError("Anthropic API request timed out")
    
    def calculate_cost(self, input_tokens: int, output_tokens: int, model: str) -> float:
        """Calculate cost for Anthropic API usage."""
        pricing = self.PRICING.get(model, self.PRICING[self.DEFAULT_MODEL])
        input_cost = (input_tokens / 1_000_000) * pricing["input"]
        output_cost = (output_tokens / 1_000_000) * pricing["output"]
        return input_cost + output_cost
    
    async def close(self) -> None:
        """Close HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None


class OpenAIAdapter(LLMAdapter):
    """Adapter for OpenAI GPT models."""
    
    # Pricing per million tokens (as of Nov 2024)
    PRICING = {
        "gpt-4-turbo": {"input": 10.0, "output": 30.0},
        "gpt-4": {"input": 30.0, "output": 60.0},
        "gpt-3.5-turbo": {"input": 0.5, "output": 1.5},
        "gpt-4o": {"input": 5.0, "output": 15.0},
        "gpt-4o-mini": {"input": 0.15, "output": 0.6},
    }
    
    DEFAULT_MODEL = "gpt-4o"
    
    def __init__(self, api_key: str, timeout: float = 120.0):
        """
        Initialize OpenAI adapter.
        
        Args:
            api_key: OpenAI API key
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None
    
    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=self.timeout,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
            )
        return self._client
    
    async def complete(self, prompt: str, model: Optional[str] = None) -> tuple[str, int, int]:
        """Generate completion using GPT."""
        model = model or self.DEFAULT_MODEL
        client = await self._get_client()
        
        try:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 4096
                }
            )
            response.raise_for_status()
            
            data = response.json()
            text = data["choices"][0]["message"]["content"]
            input_tokens = data["usage"]["prompt_tokens"]
            output_tokens = data["usage"]["completion_tokens"]
            
            return text, input_tokens, output_tokens
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise AuthenticationError("Invalid OpenAI API key")
            elif e.response.status_code == 429:
                retry_after = e.response.headers.get("retry-after")
                raise RateLimitError(
                    "OpenAI API rate limit exceeded",
                    retry_after=int(retry_after) if retry_after else None
                )
            else:
                raise
        except httpx.TimeoutException:
            raise TimeoutError("OpenAI API request timed out")
    
    def calculate_cost(self, input_tokens: int, output_tokens: int, model: str) -> float:
        """Calculate cost for OpenAI API usage."""
        pricing = self.PRICING.get(model, self.PRICING[self.DEFAULT_MODEL])
        input_cost = (input_tokens / 1_000_000) * pricing["input"]
        output_cost = (output_tokens / 1_000_000) * pricing["output"]
        return input_cost + output_cost
    
    async def close(self) -> None:
        """Close HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None


class LLMService:
    """Service for LLM operations with multiple provider support."""
    
    def __init__(
        self,
        provider: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: float = 120.0
    ):
        """
        Initialize LLM service.
        
        Args:
            provider: LLM provider ("anthropic" or "openai"). 
                     Reads from POLYHEDRA_LLM_PROVIDER env var if not provided.
            api_key: API key for the provider.
                    Reads from ANTHROPIC_API_KEY or OPENAI_API_KEY env var if not provided.
            timeout: Request timeout in seconds
        """
        # Determine provider
        if provider is None:
            provider = os.getenv("POLYHEDRA_LLM_PROVIDER", "anthropic")
        
        self.provider = provider.lower()
        
        # Determine API key
        if api_key is None:
            if self.provider == "anthropic":
                api_key = os.getenv("ANTHROPIC_API_KEY")
            elif self.provider == "openai":
                api_key = os.getenv("OPENAI_API_KEY")
        
        # Check if configured
        if not api_key:
            logger.warning(
                f"LLM service initialized without API key for provider '{self.provider}'. "
                "Service will not be functional until configured."
            )
            self._configured = False
            self._adapter: Optional[LLMAdapter] = None
            return
        
        self._configured = True
        
        # Initialize adapter
        if self.provider == "anthropic":
            self._adapter = AnthropicAdapter(api_key, timeout)
        elif self.provider == "openai":
            self._adapter = OpenAIAdapter(api_key, timeout)
        else:
            raise ValueError(
                f"Unsupported provider: {provider}. "
                "Supported providers: 'anthropic', 'openai'"
            )
        
        logger.info(f"LLM service initialized with provider: {self.provider}")
    
    @property
    def is_configured(self) -> bool:
        """Check if service is properly configured."""
        return self._configured
    
    async def complete(
        self,
        prompt: str,
        model: Optional[str] = None
    ) -> Optional[tuple[str, int, int]]:
        """
        Generate text completion.
        
        Args:
            prompt: Input prompt text
            model: Optional model name override
            
        Returns:
            Tuple of (response_text, input_tokens, output_tokens) or None if not configured
        """
        if not self._configured:
            logger.warning("LLM service not configured, skipping operation")
            return None
        
        return await self._adapter.complete(prompt, model)
    
    def estimate_tokens(self, text: str) -> int:
        """
        Estimate token count for text.
        
        Uses rough heuristic: ~4 characters per token for English text.
        
        Args:
            text: Text to estimate tokens for
            
        Returns:
            Estimated token count
        """
        return len(text) // 4
    
    def calculate_cost(
        self,
        input_tokens: int,
        output_tokens: int,
        model: Optional[str] = None
    ) -> float:
        """
        Calculate cost for token usage.
        
        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            model: Model name (uses default if not specified)
            
        Returns:
            Cost in USD
        """
        if not self._configured:
            return 0.0
        
        if model is None:
            if self.provider == "anthropic":
                model = AnthropicAdapter.DEFAULT_MODEL
            else:
                model = OpenAIAdapter.DEFAULT_MODEL
        
        return self._adapter.calculate_cost(input_tokens, output_tokens, model)
    
    async def close(self) -> None:
        """Close service and cleanup resources."""
        if self._adapter:
            await self._adapter.close()
