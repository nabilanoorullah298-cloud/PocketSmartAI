import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# Tried in order. If a model is busy or retired, the next one is used.
GEMINI_MODELS = ["gemini-flash-latest", "gemini-3.1-flash-lite"]

# Secret used to sign login tokens. Put your own SECRET_KEY line in .env.
SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key-in-env")
TOKEN_HOURS = 8
DB_PATH = "pocketsmart.db"
