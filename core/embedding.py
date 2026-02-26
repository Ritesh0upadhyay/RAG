# ingestion/embedding_generator.py
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from config/.env
env_path = Path(__file__).parent.parent / "config" / ".env"
load_dotenv(dotenv_path=env_path)

from .gemini_configuration import EMBEDDING_MODEL
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))



def generate_embedding(text):
    result = genai.embed_content(
        model=EMBEDDING_MODEL,
        content=text
    )
    return result["embedding"]
