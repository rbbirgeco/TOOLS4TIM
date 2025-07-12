"""
Error handling and retry logic for the Neural Coding Assistant.
"""

import asyncio
import logging
from typing import Dict, Any, Optional, Callable
from functools import wraps

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TaskExecutionError(Exception):
    """Custom exception for task execution failures."""
    pass

class RetryConfig:
    """Configuration for retry logic."""
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0, timeout: float = 30.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.timeout = timeout

async def with_timeout_and_retry(
    func: Callable,
    *args,
    retry_config: RetryConfig = None,
    fallback_func: Callable = None,
    **kwargs
) -> Any:
    """Execute function with timeout and retry logic."""
    if retry_config is None:
        retry_config = RetryConfig()
    
    last_exception = None
    
    for attempt in range(retry_config.max_retries + 1):
        try:
            # Apply timeout to the function
            result = await asyncio.wait_for(
                func(*args, **kwargs),
                timeout=retry_config.timeout
            )
            
            if attempt > 0:
                logger.info(f"Function succeeded on attempt {attempt + 1}")
            
            return result
            
        except asyncio.TimeoutError as e:
            last_exception = e
            logger.warning(f"Timeout on attempt {attempt + 1}/{retry_config.max_retries + 1}")
            
        except Exception as e:
            last_exception = e
            logger.warning(f"Error on attempt {attempt + 1}/{retry_config.max_retries + 1}: {str(e)}")
        
        # Wait before retry (exponential backoff)
        if attempt < retry_config.max_retries:
            delay = retry_config.base_delay * (2 ** attempt)
            await asyncio.sleep(delay)
    
    # All retries failed, try fallback if available
    if fallback_func:
        try:
            logger.info("Attempting fallback function")
            return await fallback_func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Fallback also failed: {str(e)}")
    
    # No more options, raise the last exception
    raise TaskExecutionError(f"Task failed after {retry_config.max_retries + 1} attempts: {str(last_exception)}")

def handle_errors(fallback_message: str = None):
    """Decorator for basic error handling with fallback messages."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error in {func.__name__}: {str(e)}")
                if fallback_message:
                    return fallback_message
                return f"[ERROR]: {func.__name__} failed: {str(e)}"
        return wrapper
    return decorator

async def safe_subprocess_call(command: list, timeout: float = 30.0) -> tuple[str, str, int]:
    """Safely execute subprocess with timeout and error handling."""
    try:
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await asyncio.wait_for(
            process.communicate(),
            timeout=timeout
        )
        
        return stdout.decode(), stderr.decode(), process.returncode
        
    except asyncio.TimeoutError:
        if 'process' in locals():
            process.terminate()
            await process.wait()
        raise TaskExecutionError(f"Command timed out after {timeout} seconds")
    
    except Exception as e:
        raise TaskExecutionError(f"Subprocess execution failed: {str(e)}")

class CircuitBreaker:
    """Simple circuit breaker for failing services."""
    
    def __init__(self, failure_threshold: int = 5, recovery_timeout: float = 60.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    async def call(self, func: Callable, *args, **kwargs):
        """Execute function through circuit breaker."""
        if self.state == "OPEN":
            if self.last_failure_time and (
                asyncio.get_event_loop().time() - self.last_failure_time > self.recovery_timeout
            ):
                self.state = "HALF_OPEN"
                logger.info("Circuit breaker moving to HALF_OPEN state")
            else:
                raise TaskExecutionError("Circuit breaker is OPEN - service unavailable")
        
        try:
            result = await func(*args, **kwargs)
            
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                self.failure_count = 0
                logger.info("Circuit breaker reset to CLOSED state")
            
            return result
            
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = asyncio.get_event_loop().time()
            
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
                logger.warning(f"Circuit breaker opened after {self.failure_count} failures")
            
            raise e
