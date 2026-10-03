from functools import lru_cache

from config import (
    LOCAL_EXPLANATION_MODEL,
    USE_LOCAL_EXPLANATION,
)

from ai_client import generate_text


# ---------------------------------------------------------
# LOAD LOCAL MODEL
# ---------------------------------------------------------

@lru_cache(maxsize=1)
def load_local_model():

    from transformers import pipeline

    return pipeline(
        "text2text-generation",
        model=LOCAL_EXPLANATION_MODEL,
        device=-1
    )


# ---------------------------------------------------------
# LOCAL EXPLANATION
# ---------------------------------------------------------

def local_explanation(
    topic: str
) -> str:

    generator = load_local_model()

    prompt = f"""
Explain this educational topic to a beginner.

Use:

- Simple language
- Short sentences
- Step-by-step explanation
- One simple example

Topic:

{topic}
"""

    result = generator(
        prompt,
        max_new_tokens=220,
        do_sample=False
    )

    return result[0][
        "generated_text"
    ].strip()


# ---------------------------------------------------------
# MAIN EXPLANATION FUNCTION
# ---------------------------------------------------------

async def explain_topic(
    topic: str
) -> str:

    # Try local model first
    if USE_LOCAL_EXPLANATION:

        try:

            return local_explanation(
                topic
            )

        except Exception:

            # Fall back to Gemini
            pass


    # Gemini fallback
    prompt = f"""
Explain the following topic to a beginner.

Structure your answer like this:

1. Simple definition
2. Step-by-step explanation
3. Important points
4. Simple example

Avoid unnecessary technical jargon.

Topic:

{topic}
"""

    return generate_text(
        prompt,
        temperature=0.25,
        max_output_tokens=900
    )