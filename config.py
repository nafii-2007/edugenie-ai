import os
from pathlib import Path

from dotenv import load_dotenv


# Project directory
BASE_DIR = Path(__file__).resolve().parent


# Load .env
load_dotenv(BASE_DIR / ".env")


# Gemini configuration
GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY",
    ""
).strip()


GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.8-flash"
)


# Local explanation model
LOCAL_EXPLANATION_MODEL = os.getenv(
    "LOCAL_EXPLANATION_MODEL",
    "MBZUAI/LaMini-Flan-T5-783M"
)


USE_LOCAL_EXPLANATION = (
    os.getenv(
        "USE_LOCAL_EXPLANATION",
        "true"
    ).lower()
    == "true"
)


# Maximum user input
MAX_INPUT_CHARS = int(
    os.getenv(
        "MAX_INPUT_CHARS",
        "12000"
    )
)