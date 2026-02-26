# RAG Search Backend - Deployment Package

This folder contains all the files needed to deploy the RAG searching functionality on Render.

## 📁 Folder Structure

```
search/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── Procfile                    # Render deployment config
├── runtime.txt                 # Python version specification
├── .gitignore                  # Git ignore rules
├── README.md                   # This file
│
├── core/                       # Core search modules
│   ├── __init__.py
│   ├── hybrid_retrieve.py      # Combines PostgreSQL + Semantic search
│   ├── query_metadata_by_question.py  # PostgreSQL full-text search
│   ├── sementic_search.py      # Vector similarity ranking
│   ├── gemini_configuration.py # Gemini LLM configuration
│   └── embedding.py            # Embedding generation
│
├── templates/                  # Frontend files
│   └── index.html              # Web UI
│
├── config/                     # Configuration
│   └── .env                    # Environment variables (DO NOT COMMIT)
│
└── chromadb_storage/           # Vector database storage
    └── (database files)
```

## 🔄 Search Flow

1. **User Query** → Frontend (index.html)
2. **PostgreSQL FTS** → `query_metadata_by_question.py` searches for keywords
3. **Semantic Ranking** → `semantic_search.py` ranks results using embeddings
4. **LLM Generation** → `gemini_configuration.py` generates answer
5. **Response** → Frontend displays answer + sources

## 🚀 Deployment on Render

### Step 1: Prepare Your Repository
```bash
cd search/
git init
git add .
git commit -m "Initial RAG backend setup"
git remote add origin <your-repo-url>
git push origin main
```

### Step 2: Create Render Web Service
1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Select the `search` folder as root directory
5. Set Build Command: `pip install -r requirements.txt`
6. Set Start Command: `gunicorn app:app`

### Step 3: Set Environment Variables in Render Dashboard
Navigate to "Environment" and add:
- `GOOGLE_API_KEY` - Your Gemini API key
- `DATABASE_URL` - PostgreSQL connection string
- `CHROMADB_PATH` - ./chromadb_storage

### Step 4: Deploy
Click "Deploy" - Render will automatically build and start your app.

## 📝 File Descriptions

### Core Files
- **app.py** - Flask server handling `/api/ask` endpoint
- **requirements.txt** - All Python packages needed
- **Procfile** - Tells Render to run with Gunicorn
- **runtime.txt** - Specifies Python 3.11.7

### Core Module Files
- **hybrid_retrieve.py** - Orchestrates the complete search & ranking flow
- **query_metadata_by_question.py** - PostgreSQL full-text search
- **sementic_search.py** - Vector similarity computation using cosine distance
- **gemini_configuration.py** - Gemini LLM model configuration
- **embedding.py** - Generates embeddings using Gemini API

### Frontend
- **index.html** - Complete web UI with JavaScript for API communication

## ⚙️ Configuration

Create `config/.env` with:
```
GOOGLE_API_KEY=your_gemini_api_key
DATABASE_URL=postgresql://user:password@host:5432/dbname
CHROMADB_PATH=./chromadb_storage
```

## 🔑 Important Notes

1. **Never commit `.env` file** - Add credentials in Render dashboard
2. **Database must be accessible** - Render needs to connect to your PostgreSQL
3. **Chromadb data** - Will be created at runtime in `chromadb_storage/`
4. **API Endpoint** - Available at `https://your-app.onrender.com/api/ask`

## 📡 API Endpoint

**POST** `/api/ask`

Request:
```json
{
  "question": "What is an API?"
}
```

Response:
```json
{
  "question": "What is an API?",
  "answer": "An API is...",
  "chunks_used": 3,
  "sources": [
    {
      "id": "chunk-id-1",
      "content": "First 200 chars of chunk..."
    }
  ]
}
```

## 🐛 Troubleshooting

- **Database connection failed** - Check DATABASE_URL in Render dashboard
- **API key error** - Verify GOOGLE_API_KEY is set correctly
- **No chunks found** - Ensure Chromadb database has data and PostgreSQL has metadata

---

Ready to deploy? Just push the `search/` folder to GitHub and follow the Render deployment steps above!
