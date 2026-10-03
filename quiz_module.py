import json

from ai_client import generate_text
from schemas import QuizQuestion


# ---------------------------------------------------------
# CLEAN GEMINI JSON
# ---------------------------------------------------------

def clean_json(
    raw: str
) -> str:

    raw = raw.strip()

    # Remove markdown code fences
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


# ---------------------------------------------------------
# GENERATE QUIZ
# ---------------------------------------------------------

async def generate_quiz(
    content: str
) -> list[QuizQuestion]:

    prompt = f"""
You are an educational quiz generator.

Create EXACTLY 3 multiple-choice questions from the
content below.

Return ONLY valid JSON.

The JSON must be an array containing exactly 3 objects.

Each object MUST contain:

question
options
correct_answer
explanation

Rules:

- Each question must have exactly 4 options.
- correct_answer must exactly match one option.
- Questions should test understanding.
- Distractors should be plausible.
- Do not use information outside the supplied content.

Content:

{content}
"""

    raw = generate_text(
        prompt,
        temperature=0.4,
        max_output_tokens=1600
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
            "Quiz response is not a list."
        )

    if len(data) != 3:

        raise ValueError(
            "The AI did not return exactly 3 questions."
        )

    questions = []

    for item in data:

        question = QuizQuestion.model_validate(
            item
        )

        if question.correct_answer not in question.options:

            raise ValueError(
                "Correct answer does not match an option."
            )

        questions.append(
            question
        )

    return questions