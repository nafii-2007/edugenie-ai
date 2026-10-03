from ai_client import generate_text


async def summarize_text(
    text: str
) -> str:

    prompt = f"""
You are EduGenie, an educational summarization assistant.

Summarize the following educational text.

Requirements:

- Preserve important facts.
- Preserve definitions.
- Preserve important relationships.
- Preserve important examples.
- Remove repetition.
- Use simple student-friendly language.
- Do not introduce facts that are not present in the input.
- Use bullet points where useful.

Educational text:

{text}

Summary:
"""

    return generate_text(
        prompt,
        temperature=0.2,
        max_output_tokens=900
    )