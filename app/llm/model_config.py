import os
from dotenv import load_dotenv

load_dotenv()

# Temporarily mocked/disabled due to Gemini free-tier quota limits during development testing.
DEFAULT_MODEL = "models/gemini-2.0-flash"


def get_model_name() -> str:
    """Return the disabled/mock model name during development testing."""
    return DEFAULT_MODEL


def configure_genai(api_key: str | None = None) -> None:
    """Gemini configuration disabled during quota testing."""
    return None