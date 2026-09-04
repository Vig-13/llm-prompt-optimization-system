import time

from google import genai

from app.config import GEMINI_API_KEY


# ============================================================
# Gemini client configuration
# ============================================================

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# Keep the model name centralized.
MODEL_NAME = "gemini-3.5-flash-lite"


# Maximum number of retries after the initial request.
MAX_RETRIES = 3


# Initial delay before retrying.
INITIAL_RETRY_DELAY = 2


# Retry only temporary/rate-limit errors.
RETRYABLE_STATUS_CODES = {
    429,
    503
}


def generate_content(
    contents,
    model=MODEL_NAME
):
    """
    Generate Gemini content with retry handling.

    Handles:
        429 - Rate limit / quota-related temporary failure
        503 - Service temporarily unavailable

    Uses exponential backoff:

        2 seconds
        4 seconds
        8 seconds

    Raises the final exception if all retries fail.
    """

    last_error = None


    for attempt in range(
        MAX_RETRIES + 1
    ):

        try:

            response = client.models.generate_content(
                model=model,
                contents=contents
            )

            return response


        except Exception as error:

            last_error = error


            error_text = str(
                error
            ).lower()


            # ------------------------------------------------
            # Determine whether this looks like a retryable
            # Gemini API error.
            # ------------------------------------------------

            is_retryable = any(
                str(status_code) in error_text
                for status_code in RETRYABLE_STATUS_CODES
            )


            if not is_retryable:

                raise


            # ------------------------------------------------
            # If this was the final attempt, stop retrying.
            # ------------------------------------------------

            if attempt >= MAX_RETRIES:

                raise RuntimeError(
                    "Gemini API request failed after "
                    f"{MAX_RETRIES} retries.\n\n"
                    f"Last error: {error}"
                ) from error


            # ------------------------------------------------
            # Exponential backoff
            #
            # attempt 0 → 2 seconds
            # attempt 1 → 4 seconds
            # attempt 2 → 8 seconds
            # ------------------------------------------------

            delay = (
                INITIAL_RETRY_DELAY
                * (2 ** attempt)
            )


            print(
                "\nGemini API request failed "
                f"(attempt {attempt + 1}/"
                f"{MAX_RETRIES + 1})."
            )


            print(
                f"Retrying in {delay} seconds..."
            )


            time.sleep(
                delay
            )


    # This should never normally be reached,
    # but provides a safe fallback.

    raise RuntimeError(
        "Gemini API request failed."
    ) from last_error