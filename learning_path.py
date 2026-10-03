import json

from ai_client import generate_text
from schemas import LearningStep


def clean_json(
    raw: str
) -> str:

    raw = raw.strip()

    if raw.startswith("```"):

        lines = raw.splitlines()

        if lines:
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        raw = "\n".join(
            lines
        ).strip()

    return raw


async def get_learning_recommendations(
    topic: str
) -> list[LearningStep]:

    prompt = f"""
You are EduGenie, a personalized learning assistant.

Create a structured learning path for:

{topic}

Return ONLY valid JSON.

Return an array of objects.

Each object must contain:

level
topics
timeline
resources

Use these levels:

Beginner
Intermediate
Advanced

Requirements:

- Beginner should establish fundamentals.
- Intermediate should build practical knowledge.
- Advanced should cover deeper concepts.
- Topics must be arrays.
- Resources must be practical suggestions.
- Do not invent specific URLs.
- Make the progression logical.
- Give realistic timelines.
"""

    raw = generate_text(
        prompt,
        temperature=0.3,
        max_output_tokens=1400
    )

    cleaned = clean_json(
        raw
    )

    data = json.loads(
        cleaned
    )

    if not isinstance(
        data,
        list
    ):

        raise ValueError(
            "Learning path response is invalid."
        )

    return [
        LearningStep.model_validate(
            item
        )
        for item in data
    ]