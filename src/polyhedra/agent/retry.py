"""Retry strategy with exponential backoff and circuit breaker."""
from dataclasses import dataclass
from typing import Callable, Any, Optional, TypeVar
import asyncio
import logging
import random
import time

logger = logging.getLogger(__name__)

T = TypeVar('T')


@dataclass
class RetryConfig:
    """Configuration for retry behavior."""
    max_attempts: int = 3
    initial_delay: float = 1.0
    max_delay: float = 60.0
    exponential_base: float = 2.0
    jitter: bool = True


class CircuitBreaker:
    """Prevents infinite retry loops by tracking failures."""
    
    def __init__(self, failure_threshold: int = 5, timeout: float = 60.0):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failures = 0
        self.last_failure_time: Optional[float] = None
        self.state = "closed"  # closed (normal), open (blocking), half-open (testing)
        
    def record_success(self) -> None:
        """Record successful operation."""
        self.failures = 0
        self.state = "closed"
        
    def record_failure(self) -> None:
        """Record failed operation."""
        self.failures += 1
        self.last_failure_time = time.time()
        
        if self.failures >= self.failure_threshold:
            self.state = "open"
            logger.warning(
                f"Circuit breaker opened after {self.failures} failures"
            )
            
    def can_attempt(self) -> bool:
        """Check if operation can be attempted."""
        if self.state == "closed":
            return True
            
        if self.state == "open":
            # Check if timeout has passed
            if self.last_failure_time and \
               time.time() - self.last_failure_time >= self.timeout:
                self.state = "half-open"
                logger.info("Circuit breaker entering half-open state")
                return True
            return False
            
        # half-open state - allow one attempt
        return True
        
    def reset(self) -> None:
        """Reset circuit breaker."""
        self.failures = 0
        self.state = "closed"
        self.last_failure_time = None


async def retry_with_backoff(
    func: Callable[[], Any],
    config: RetryConfig,
    circuit_breaker: Optional[CircuitBreaker] = None
) -> Any:
    """Execute function with exponential backoff retry.
    
    Args:
        func: Async function to execute
        config: Retry configuration
        circuit_breaker: Optional circuit breaker for failure tracking
        
    Returns:
        Result from successful function execution
        
    Raises:
        Exception: Last exception if all retries exhausted
    """
    last_exception = None
    
    for attempt in range(config.max_attempts):
        # Check circuit breaker
        if circuit_breaker and not circuit_breaker.can_attempt():
            raise Exception("Circuit breaker is open - too many failures")
            
        try:
            result = await func()
            
            # Success - record and return
            if circuit_breaker:
                circuit_breaker.record_success()
            
            if attempt > 0:
                logger.info(f"Succeeded after {attempt + 1} attempts")
                
            return result
            
        except Exception as e:
            last_exception = e
            
            if circuit_breaker:
                circuit_breaker.record_failure()
                
            # Don't retry on last attempt
            if attempt == config.max_attempts - 1:
                logger.error(
                    f"Failed after {config.max_attempts} attempts: {e}"
                )
                break
                
            # Calculate delay with exponential backoff
            delay = min(
                config.initial_delay * (config.exponential_base ** attempt),
                config.max_delay
            )
            
            # Add jitter if enabled
            if config.jitter:
                delay = delay * (0.5 + random.random() * 0.5)
                
            logger.warning(
                f"Attempt {attempt + 1} failed: {e}. "
                f"Retrying in {delay:.2f}s..."
            )
            
            await asyncio.sleep(delay)
            
    # All retries exhausted
    raise last_exception
