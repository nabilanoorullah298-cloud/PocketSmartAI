import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# Tried in order. If a model is busy or retired, the next one is used.
GEMINI_MODELS = ["gemini-flash-latest", "gemini-3.1-flash-lite"]
