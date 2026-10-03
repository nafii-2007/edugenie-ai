import time
from functools import lru_cache

from google import genai
from google.genai import types

from config import GEMINI_API_KEY, GEMINI_MODEL, MAX_INPUT_CHARS


class AIConfigurationError(RuntimeError):
    pass


@lru_cache(maxsize=1)
def get_client():
    if not GEMINI_API_KEY:
        raise AIConfigurationError(
            "GEMINI_API_KEY is not configured. "
            "Create a .env file and add your Gemini API key."
        )

    return genai.Client(api_key=GEMINI_API_KEY)


def generate_text(
    prompt: str,
    *,
    temperature: float = 0.4,
    max_output_tokens: int = 1200,
) -> str:

    prompt = prompt.strip()

    if not prompt:
        raise ValueError("Input cannot be empty.")

    if len(prompt) > MAX_INPUT_CHARS:
        raise ValueError(
            f"Input is too long. "
            f"Maximum allowed is {MAX_INPUT_CHARS} characters."
        )

    client = get_client()

    max_retries = 3

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=temperature,
                    max_output_tokens=max_output_tokens,
                ),
            )

            text = (response.text or "").strip()

            if not text:
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            return text

        except Exception as error:

            error_text = str(error)

            # Gemini 503 = temporary server overload.
            if "503" in error_text or "UNAVAILABLE" in error_text:

                if attempt < max_retries - 1:

                    wait_time = 2 ** attempt

                    print(
                        f"Gemini temporarily unavailable. "
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                    continue

            raise

    raise RuntimeError(
        "Gemini is temporarily unavailable. "
        "Please try again in a few seconds."
    )