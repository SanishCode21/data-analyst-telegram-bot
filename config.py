import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("BOT_TOKEN")
AIPIPE_TOKEN = os.getenv("AI_TOKEN")
LOG_URL = os.getenv("LOG_URL")

MODEL_NAME = "gpt-5-mini"
BASE_URL = "https://aipipe.org/openai/v1"

LOG_FILE = "run.jsonl"
MAX_HISTORY = 6

