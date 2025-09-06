import os
from dotenv import load_dotenv


load_dotenv()

BASE_URL = "http://127.0.0.1:8000/api"
BOT_SECRET = os.getenv("BOT_SHARED_SECRET")     


def _headers():
    h = {}
    if BOT_SECRET:
        h["X-Bot-Secret"] = BOT_SECRET
    return h
