from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import logging

logger = logging.getLogger("RAG-Retry")

def api_retry_decorator(max_attempts: int = 3):
    """
    Standard Tenacity retry decorator for external network API calls (like OpenRouter).
    Retries on ConnectionError or TimeoutError with exponential backoff.
    """
    return retry(
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((ConnectionError, TimeoutError)),
        before_sleep=lambda retry_state: logger.warning(
            f"API call failed (attempt {retry_state.attempt_number}). Retrying in {retry_state.next_action.sleep}s..."
        ),
        reraise=True
    )
