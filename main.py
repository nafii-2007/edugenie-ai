from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from schemas import (
    TextRequest,
    QAResponse,
    ExplainResponse,
    SummaryResponse,
    QuizResponse,
    LearningPathResponse,
)

from qna import answer_question
from explanation_module import explain_topic
from summary_module import summarize_text
from quiz_module import generate_quiz
from learning_path import get_learning_recommendations


# ---------------------------------------------------------
# Create FastAPI application
# ---------------------------------------------------------

app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0",
)


# ---------------------------------------------------------
# Static files and HTML templates
# ---------------------------------------------------------

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)

templates = Jinja2Templates(
    directory="templates"
)


# ---------------------------------------------------------
# Home page
# ---------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request},
    )


# ---------------------------------------------------------
# Health check
# ---------------------------------------------------------

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "EduGenie"
    }


# ---------------------------------------------------------
# Question & Answer
# ---------------------------------------------------------

@app.post("/qa", response_model=QAResponse)
async def qa(payload: TextRequest):
    answer = await answer_question(payload.text)

    return QAResponse(
        answer=answer
    )


# ---------------------------------------------------------
# Explain a topic
# ---------------------------------------------------------

@app.post("/explain", response_model=ExplainResponse)
async def explain(payload: TextRequest):
    explanation = await explain_topic(payload.text)

    return ExplainResponse(
        explanation=explanation
    )


# ---------------------------------------------------------
# Generate quiz
# ---------------------------------------------------------

@app.post("/quiz", response_model=QuizResponse)
async def quiz(payload: TextRequest):
    questions = await generate_quiz(payload.text)

    return QuizResponse(
        questions=questions
    )


# ---------------------------------------------------------
# Summarize text
# ---------------------------------------------------------

@app.post("/summarize", response_model=SummaryResponse)
async def summarize(payload: TextRequest):
    summary = await summarize_text(payload.text)

    return SummaryResponse(
        summary=summary
    )


# ---------------------------------------------------------
# Learning path recommendations
# ---------------------------------------------------------

@app.post(
    "/learn/recommendations",
    response_model=LearningPathResponse
)
async def learning_recommendations(payload: TextRequest):
    recommendations = await get_learning_recommendations(
        payload.text
    )

    return LearningPathResponse(
        recommendations=recommendations
    )