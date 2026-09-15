import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
MONGO_URI = os.getenv("MONGO_URI")
FRONTEND_URL = os.getenv("FRONTEND_URL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
required_settings = {
    "GROQ_API_KEY": GROQ_API_KEY,
    "GEMINI_API_KEY": GEMINI_API_KEY,
    "PINECONE_API_KEY": PINECONE_API_KEY,
    "PINECONE_INDEX_NAME": PINECONE_INDEX_NAME,
    "MONGO_URI": MONGO_URI,
    "FRONTEND_URL": FRONTEND_URL,
    "ADMIN_PASSWORD":ADMIN_PASSWORD
}

for name, value in required_settings.items():
    if not value:
        raise RuntimeError(f"{name} is not configured")
