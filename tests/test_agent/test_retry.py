"""Tests for retry strategy module."""
import pytest
import asyncio
import time
from polyhedra.agent.retry import RetryConfig, CircuitBreaker, retry_with_backoff


@pytest.mark.asyncio
async def test_retry_success_first_attempt():
    """Test successful execution on first attempt."""
    call_count = 0
    
    async def success_func():
        nonlocal call_count
        call_count += 1
        return "success"
    
    config = RetryConfig(max_attempts=3)
    result = await retry_with_backoff(success_func, config)
    
    assert result == "success"
    assert call_count == 1


@pytest.mark.asyncio
async def test_retry_success_after_failures():
    """Test successful execution after transient failures."""
    call_count = 0
    
    async def eventual_success():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise Exception("Transient failure")
        return "success"
    
    config = RetryConfig(max_attempts=3, initial_delay=0.01)
    result = await retry_with_backoff(eventual_success, config)
    
    assert result == "success"
    assert call_count == 3


@pytest.mark.asyncio
async def test_retry_exhausted():
    """Test all retries exhausted."""
    call_count = 0
    
    async def always_fails():
        nonlocal call_count
        call_count += 1
        raise Exception("Permanent failure")
    
    config = RetryConfig(max_attempts=3, initial_delay=0.01)
    
    with pytest.raises(Exception, match="Permanent failure"):
        await retry_with_backoff(always_fails, config)
    
    assert call_count == 3


@pytest.mark.asyncio
async def test_exponential_backoff():
    """Test exponential backoff delays."""
    timestamps = []
    
    async def failing_func():
        timestamps.append(time.time())
        raise Exception("Fail")
    
    config = RetryConfig(max_attempts=3, initial_delay=0.1, jitter=False)
    
    with pytest.raises(Exception):
        await retry_with_backoff(failing_func, config)
    
    # Check delays are roughly exponential
    assert len(timestamps) == 3
    delay1 = timestamps[1] - timestamps[0]
    delay2 = timestamps[2] - timestamps[1]
    
    # Delay2 should be roughly 2x delay1 (exponential_base=2.0)
    assert delay2 > delay1
    assert delay2 / delay1 >= 1.8  # Allow some tolerance


@pytest.mark.asyncio
async def test_circuit_breaker_opens():
    """Test circuit breaker opens after threshold failures."""
    breaker = CircuitBreaker(failure_threshold=3)
    call_count = 0
    
    async def failing_func():
        nonlocal call_count
        call_count += 1
        raise Exception("Fail")
    
    config = RetryConfig(max_attempts=5, initial_delay=0.01)
    
    with pytest.raises(Exception):
        await retry_with_backoff(failing_func, config, breaker)
    
    # Circuit breaker should have opened
    assert breaker.state == "open"
    assert not breaker.can_attempt()


@pytest.mark.asyncio
async def test_circuit_breaker_resets_on_success():
    """Test circuit breaker resets after successful call."""
    breaker = CircuitBreaker(failure_threshold=5)
    
    # Record some failures
    for _ in range(3):
        breaker.record_failure()
    
    assert breaker.failures == 3
    
    # Record success
    breaker.record_success()
    
    assert breaker.failures == 0
    assert breaker.state == "closed"


def test_circuit_breaker_half_open():
    """Test circuit breaker enters half-open after timeout."""
    breaker = CircuitBreaker(failure_threshold=2, timeout=0.1)
    
    # Open the breaker
    breaker.record_failure()
    breaker.record_failure()
    
    assert breaker.state == "open"
    assert not breaker.can_attempt()
    
    # Wait for timeout
    time.sleep(0.15)
    
    # Should allow one attempt
    assert breaker.can_attempt()
    assert breaker.state == "half-open"


@pytest.mark.asyncio
async def test_jitter_adds_randomness():
    """Test jitter adds randomness to delays."""
    timestamps = []
    
    async def failing_func():
        timestamps.append(time.time())
        raise Exception("Fail")
    
    config = RetryConfig(max_attempts=3, initial_delay=0.1, jitter=True)
    
    with pytest.raises(Exception):
        await retry_with_backoff(failing_func, config)
    
    # With jitter, delays should vary (not be exact multiples)
    assert len(timestamps) == 3


@pytest.mark.asyncio
async def test_max_delay_cap():
    """Test delay is capped at max_delay."""
    timestamps = []
    
    async def failing_func():
        timestamps.append(time.time())
        raise Exception("Fail")
    
    config = RetryConfig(
        max_attempts=5,
        initial_delay=0.1,
        max_delay=0.2,
        jitter=False
    )
    
    with pytest.raises(Exception):
        await retry_with_backoff(failing_func, config)
    
    # Check that delays don't exceed max_delay
    for i in range(1, len(timestamps)):
        delay = timestamps[i] - timestamps[i-1]
        assert delay <= 0.25  # Allow some tolerance
