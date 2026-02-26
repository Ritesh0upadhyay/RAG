import psycopg2
from dotenv import load_dotenv
from pathlib import Path
import os

# Load environment variables from config/.env
env_path = Path(__file__).parent.parent / "config" / ".env"
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")

def search_metadata(user_query, top_k=5):
    """Search metadata in PostgreSQL and return top chunk_ids only."""
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # Use ILIKE for question and cast JSONB to text for keywords search
    sql = f"""
        SELECT chunk_id
              FROM chunks_metadata
              WHERE keywords::text ILIKE %s
              OR question::text ILIKE %s
              ORDER BY created_at DESC
              LIMIT {top_k}
    """
    cur.execute(sql, (f"%{user_query}%", f"%{user_query}%"))
    results = cur.fetchall()

    conn.close()

    # Extract only chunk_ids
    chunk_ids = [r[0] for r in results]
    return chunk_ids
