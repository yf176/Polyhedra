"""Unit tests for LLM service."""

import os
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from polyhedra.services.llm_service import (
    AnthropicAdapter,
    AuthenticationError,
    ConfigurationError,
    LLMService,
    OpenAIAdapter,
    RateLimitError,
    TimeoutError,
)


@pytest.fixture
def mock_anthropic_response():
    """Mock Anthropic API response."""
    return {
        "content": [{"text": "This is a test response from Claude."}],
        "usage": {"input_tokens": 10, "output_tokens": 20},
    }


@pytest.fixture
def mock_openai_response():
    """Mock OpenAI API response."""
    return {
        "choices": [{"message": {"content": "This is a test response from GPT."}}],
        "usage": {"prompt_tokens": 10, "completion_tokens": 20},
    }


class TestAnthropicAdapter:
    """Tests for Anthropic adapter."""
    
    @pytest.mark.asyncio
    async def test_complete_success(self, mock_anthropic_response):
        """Test successful completion with Anthropic."""
        adapter = AnthropicAdapter(api_key="test_key")
        
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.json.return_value = mock_anthropic_response
        mock_response.raise_for_status = MagicMock()
        mock_client.post.return_value = mock_response
        
        adapter._client = mock_client
        
        text, input_tokens, output_tokens = await adapter.complete("test prompt")
        
        assert text == "This is a test response from Claude."
        assert input_tokens == 10
        assert output_tokens == 20
        mock_client.post.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_complete_with_custom_model(self, mock_anthropic_response):
        """Test completion with custom model."""
        adapter = AnthropicAdapter(api_key="test_key")
        
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.json.return_value = mock_anthropic_response
        mock_response.raise_for_status = MagicMock()
        mock_client.post.return_value = mock_response
        
        adapter._client = mock_client
        
        await adapter.complete("test prompt", model="claude-3-haiku-20240307")
        
        call_args = mock_client.post.call_args
        assert call_args[1]["json"]["model"] == "claude-3-haiku-20240307"
    
    @pytest.mark.asyncio
    async def test_complete_authentication_error(self):
        """Test handling of authentication errors."""
        adapter = AnthropicAdapter(api_key="invalid_key")
        
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_client.post.side_effect = httpx.HTTPStatusError(
            "401 Unauthorized", request=MagicMock(), response=mock_response
        )
        
        adapter._client = mock_client
        
        with pytest.raises(AuthenticationError, match="Invalid Anthropic API key"):
            await adapter.complete("test prompt")
    
    @pytest.mark.asyncio
    async def test_complete_rate_limit_error(self):
        """Test handling of rate limit errors."""
        adapter = AnthropicAdapter(api_key="test_key")
        
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.headers = {"retry-after": "60"}
        mock_client.post.side_effect = httpx.HTTPStatusError(
            "429 Too Many Requests", request=MagicMock(), response=mock_response
        )
        
        adapter._client = mock_client
        
        with pytest.raises(RateLimitError, match="rate limit exceeded") as exc_info:
            await adapter.complete("test prompt")
        
        assert exc_info.value.retry_after == 60
    
    @pytest.mark.asyncio
    async def test_complete_timeout_error(self):
        """Test handling of timeout errors."""
        adapter = AnthropicAdapter(api_key="test_key")
        
        mock_client = AsyncMock()
        mock_client.post.side_effect = httpx.TimeoutException("Request timed out")
        
        adapter._client = mock_client
        
        with pytest.raises(TimeoutError, match="timed out"):
            await adapter.complete("test prompt")
    
    def test_calculate_cost_default_model(self):
        """Test cost calculation for default model."""
        adapter = AnthropicAdapter(api_key="test_key")
        
        # Claude 3.5 Sonnet: $3/M input, $15/M output
        cost = adapter.calculate_cost(1000, 2000, "claude-3-5-sonnet-20241022")
        
        expected = (1000 / 1_000_000 * 3.0) + (2000 / 1_000_000 * 15.0)
        assert abs(cost - expected) < 0.0001
    
    def test_calculate_cost_opus(self):
        """Test cost calculation for Opus model."""
        adapter = AnthropicAdapter(api_key="test_key")
        
        # Claude 3 Opus: $15/M input, $75/M output
        cost = adapter.calculate_cost(1000, 2000, "claude-3-opus-20240229")
        
        expected = (1000 / 1_000_000 * 15.0) + (2000 / 1_000_000 * 75.0)
        assert abs(cost - expected) < 0.0001
    
    @pytest.mark.asyncio
    async def test_close(self):
        """Test closing the adapter."""
        adapter = AnthropicAdapter(api_key="test_key")
        
        mock_client = AsyncMock()
        adapter._client = mock_client
        
        await adapter.close()
        
        mock_client.aclose.assert_called_once()
        assert adapter._client is None


class TestOpenAIAdapter:
    """Tests for OpenAI adapter."""
    
    @pytest.mark.asyncio
    async def test_complete_success(self, mock_openai_response):
        """Test successful completion with OpenAI."""
        adapter = OpenAIAdapter(api_key="test_key")
        
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.json.return_value = mock_openai_response
        mock_response.raise_for_status = MagicMock()
        mock_client.post.return_value = mock_response
        
        adapter._client = mock_client
        
        text, input_tokens, output_tokens = await adapter.complete("test prompt")
        
        assert text == "This is a test response from GPT."
        assert input_tokens == 10
        assert output_tokens == 20
        mock_client.post.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_complete_authentication_error(self):
        """Test handling of authentication errors."""
        adapter = OpenAIAdapter(api_key="invalid_key")
        
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_client.post.side_effect = httpx.HTTPStatusError(
            "401 Unauthorized", request=MagicMock(), response=mock_response
        )
        
        adapter._client = mock_client
        
        with pytest.raises(AuthenticationError, match="Invalid OpenAI API key"):
            await adapter.complete("test prompt")
    
    @pytest.mark.asyncio
    async def test_complete_rate_limit_error(self):
        """Test handling of rate limit errors."""
        adapter = OpenAIAdapter(api_key="test_key")
        
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.headers = {"retry-after": "30"}
        mock_client.post.side_effect = httpx.HTTPStatusError(
            "429 Too Many Requests", request=MagicMock(), response=mock_response
        )
        
        adapter._client = mock_client
        
        with pytest.raises(RateLimitError, match="rate limit exceeded") as exc_info:
            await adapter.complete("test prompt")
        
        assert exc_info.value.retry_after == 30
    
    def test_calculate_cost_default_model(self):
        """Test cost calculation for default model."""
        adapter = OpenAIAdapter(api_key="test_key")
        
        # GPT-4o: $5/M input, $15/M output
        cost = adapter.calculate_cost(1000, 2000, "gpt-4o")
        
        expected = (1000 / 1_000_000 * 5.0) + (2000 / 1_000_000 * 15.0)
        assert abs(cost - expected) < 0.0001
    
    def test_calculate_cost_gpt4_turbo(self):
        """Test cost calculation for GPT-4 Turbo."""
        adapter = OpenAIAdapter(api_key="test_key")
        
        # GPT-4 Turbo: $10/M input, $30/M output
        cost = adapter.calculate_cost(1000, 2000, "gpt-4-turbo")
        
        expected = (1000 / 1_000_000 * 10.0) + (2000 / 1_000_000 * 30.0)
        assert abs(cost - expected) < 0.0001


class TestLLMService:
    """Tests for LLM service."""
    
    def test_init_with_explicit_provider_anthropic(self):
        """Test initialization with explicit Anthropic provider."""
        service = LLMService(provider="anthropic", api_key="test_key")
        
        assert service.is_configured is True
        assert service.provider == "anthropic"
        assert isinstance(service._adapter, AnthropicAdapter)
    
    def test_init_with_explicit_provider_openai(self):
        """Test initialization with explicit OpenAI provider."""
        service = LLMService(provider="openai", api_key="test_key")
        
        assert service.is_configured is True
        assert service.provider == "openai"
        assert isinstance(service._adapter, OpenAIAdapter)
    
    def test_init_with_env_var_provider(self, monkeypatch):
        """Test initialization with provider from environment variable."""
        monkeypatch.setenv("POLYHEDRA_LLM_PROVIDER", "openai")
        monkeypatch.setenv("OPENAI_API_KEY", "test_key")
        
        service = LLMService()
        
        assert service.is_configured is True
        assert service.provider == "openai"
    
    def test_init_with_env_var_api_key_anthropic(self, monkeypatch):
        """Test initialization with Anthropic API key from environment."""
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test_key")
        
        service = LLMService(provider="anthropic")
        
        assert service.is_configured is True
    
    def test_init_with_env_var_api_key_openai(self, monkeypatch):
        """Test initialization with OpenAI API key from environment."""
        monkeypatch.setenv("OPENAI_API_KEY", "test_key")
        
        service = LLMService(provider="openai")
        
        assert service.is_configured is True
    
    def test_init_without_api_key(self, monkeypatch):
        """Test initialization without API key."""
        # Clear environment variables
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        
        service = LLMService(provider="anthropic")
        
        assert service.is_configured is False
        assert service._adapter is None
    
    def test_init_with_unsupported_provider(self):
        """Test initialization with unsupported provider."""
        with pytest.raises(ValueError, match="Unsupported provider"):
            LLMService(provider="palm", api_key="test_key")
    
    @pytest.mark.asyncio
    async def test_complete_when_configured(self, mock_anthropic_response):
        """Test completion when service is configured."""
        service = LLMService(provider="anthropic", api_key="test_key")
        
        mock_client = AsyncMock()
        mock_response = MagicMock()
        mock_response.json.return_value = mock_anthropic_response
        mock_response.raise_for_status = MagicMock()
        mock_client.post.return_value = mock_response
        
        service._adapter._client = mock_client
        
        result = await service.complete("test prompt")
        
        assert result is not None
        text, input_tokens, output_tokens = result
        assert text == "This is a test response from Claude."
        assert input_tokens == 10
        assert output_tokens == 20
    
    @pytest.mark.asyncio
    async def test_complete_when_not_configured(self, monkeypatch):
        """Test completion when service is not configured."""
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        
        service = LLMService(provider="anthropic")
        
        result = await service.complete("test prompt")
        
        assert result is None
    
    def test_estimate_tokens(self):
        """Test token estimation."""
        service = LLMService(provider="anthropic", api_key="test_key")
        
        text = "This is a test sentence."  # 24 chars
        tokens = service.estimate_tokens(text)
        
        assert tokens == 24 // 4  # Should be 6
    
    def test_calculate_cost_when_configured(self):
        """Test cost calculation when configured."""
        service = LLMService(provider="anthropic", api_key="test_key")
        
        cost = service.calculate_cost(1000, 2000)
        
        assert cost > 0
    
    def test_calculate_cost_when_not_configured(self, monkeypatch):
        """Test cost calculation when not configured."""
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        
        service = LLMService(provider="anthropic")
        
        cost = service.calculate_cost(1000, 2000)
        
        assert abs(cost) < 0.0001
    
    def test_calculate_cost_with_explicit_model(self):
        """Test cost calculation with explicit model."""
        service = LLMService(provider="anthropic", api_key="test_key")
        
        cost = service.calculate_cost(1000, 2000, model="claude-3-haiku-20240307")
        
        # Haiku: $0.25/M input, $1.25/M output
        expected = (1000 / 1_000_000 * 0.25) + (2000 / 1_000_000 * 1.25)
        assert abs(cost - expected) < 0.0001
    
    @pytest.mark.asyncio
    async def test_close(self):
        """Test closing the service."""
        service = LLMService(provider="anthropic", api_key="test_key")
        
        mock_adapter = AsyncMock()
        service._adapter = mock_adapter
        
        await service.close()
        
        mock_adapter.close.assert_called_once()


class TestIntegration:
    """Integration tests for LLM service."""
    
    def test_default_configuration(self, monkeypatch):
        """Test that default configuration uses Anthropic."""
        monkeypatch.delenv("POLYHEDRA_LLM_PROVIDER", raising=False)
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test_key")
        
        service = LLMService()
        
        assert service.provider == "anthropic"
        assert service.is_configured is True
    
    @pytest.mark.asyncio
    async def test_switching_providers(self, mock_anthropic_response, mock_openai_response):
        """Test that different providers work correctly."""
        # Test Anthropic
        anthropic_service = LLMService(provider="anthropic", api_key="test_key")
        assert isinstance(anthropic_service._adapter, AnthropicAdapter)
        
        # Test OpenAI
        openai_service = LLMService(provider="openai", api_key="test_key")
        assert isinstance(openai_service._adapter, OpenAIAdapter)
    
    def test_cost_calculation_accuracy(self):
        """Test that cost calculations are accurate."""
        service = LLMService(provider="anthropic", api_key="test_key")
        
        # Test with realistic token counts
        input_tokens = 50_000  # ~12k words
        output_tokens = 10_000  # ~2.5k words
        
        cost = service.calculate_cost(input_tokens, output_tokens)
        
        # Claude 3.5 Sonnet: $3/M input, $15/M output
        expected = (50_000 / 1_000_000 * 3.0) + (10_000 / 1_000_000 * 15.0)
        assert abs(cost - expected) < 0.0001
        
        # Verify cost is in expected range ($0.30 for this test)
        assert 0.25 < cost < 0.35
