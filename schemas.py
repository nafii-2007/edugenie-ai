from pydantic import BaseModel, Field


# ---------------------------------------------------------
# COMMON REQUEST
# ---------------------------------------------------------

class TextRequest(BaseModel):

    text: str = Field(
        min_length=1,
        max_length=12000
    )


# ---------------------------------------------------------
# Q&A RESPONSE
# ---------------------------------------------------------

class QAResponse(BaseModel):

    answer: str


# ---------------------------------------------------------
# EXPLANATION RESPONSE
# ---------------------------------------------------------

class ExplainResponse(BaseModel):

    explanation: str


# ---------------------------------------------------------
# SUMMARY RESPONSE
# ---------------------------------------------------------

class SummaryResponse(BaseModel):

    summary: str


# ---------------------------------------------------------
# QUIZ
# ---------------------------------------------------------

class QuizQuestion(BaseModel):

    question: str

    options: list[str] = Field(
        min_length=4,
        max_length=4
    )

    correct_answer: str

    explanation: str = ""


class QuizResponse(BaseModel):

    questions: list[QuizQuestion] = Field(
        min_length=1,
        max_length=10
    )


# ---------------------------------------------------------
# LEARNING PATH
# ---------------------------------------------------------

class LearningStep(BaseModel):

    level: str

    topics: list[str]

    timeline: str

    resources: list[str]


class LearningPathResponse(BaseModel):

    recommendations: list[LearningStep]