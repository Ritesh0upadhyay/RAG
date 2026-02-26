from flask import Flask, render_template, request, jsonify
from core.hybrid_retrieve import hybrid_retrieve
from core.gemini_configuration import metadata_model
import traceback
import sys
from pathlib import Path
from dotenv import load_dotenv
import os

# Add the RAG folder to path so core imports work
sys.path.insert(0, str(Path(__file__).parent))

# Load environment variables from config/.env
env_path = Path(__file__).parent / "config" / ".env"
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/api/ask', methods=['POST'])
def ask_question():
    """API endpoint to handle user questions"""
    try:
        data = request.json
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({'error': 'Question cannot be empty'}), 400
        
        # Step 1: Hybrid retrieval
        print(f"🔍 Searching for: {question}")
        top_chunks = hybrid_retrieve(question, fts_limit=5, top_k_semantic=3)
        
        if not top_chunks:
            return jsonify({
                'error': 'No relevant chunks found in database',
                'answer': 'Sorry, I could not find relevant information to answer your question.'
            }), 404
        
        # Step 2: Build context from chunks
        context_text = "\n\n".join([c["document"] for c in top_chunks])
        
        # Step 3: Build prompt for Gemini
        llm_prompt = f"""You are a helpful assistant. Use the following context to answer the question.

Context:
{context_text}

Question:
{question}
"""
        
        # Step 4: Call Gemini LLM
        response = metadata_model.generate_content(
            llm_prompt,
            generation_config={"temperature": 0.2, "max_output_tokens": 500}
        )
        
        answer_text = response.text
        
        # Return response with chunks for reference
        return jsonify({
            'question': question,
            'answer': answer_text,
            'chunks_used': len(top_chunks),
            'sources': [{'id': c['chunk_id'], 'content': c['document'][:200]} for c in top_chunks]
        }), 200
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
