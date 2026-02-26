from dotenv import load_dotenv
from pathlib import Path
import os
import google.generativeai as genai

# Load environment variables from config/.env
env_path = Path(__file__).parent.parent / "config" / ".env"
load_dotenv(dotenv_path=env_path)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Metadata generation model
metadata_model = genai.GenerativeModel("gemini-2.5-flash-lite")

# Embedding model name
EMBEDDING_MODEL = "gemini-embedding-001"
