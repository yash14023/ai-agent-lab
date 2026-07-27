import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

API_KEY = os.getenv("ZEN_API_KEY")
MODEL = "deepseek-v4-flash-free"
BASE_URL = "https://opencode.ai/zen/v1"
