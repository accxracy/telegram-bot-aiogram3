import os
from dotenv import load_dotenv


load_dotenv()
URL = os.getenv("URL")

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("NEURO_API_KEY")
ADMIN_ID = os.getenv("ADMIN_ID")

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "postgres")



