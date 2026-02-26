"""
Hybrid Retrieval: Combines Full-Text Search (PostgreSQL) + Semantic Ranking (Chroma)
"""
import chromadb
from .query_metadata_by_question import search_metadata
from .sementic_search import semantic_rank

# Initialize Chroma client
client = chromadb.PersistentClient(path="./chromadb_storage")
collection = client.get_or_create_collection(name="document_vectors")


def hybrid_retrieve(question, fts_limit=5, top_k_semantic=3):
    """
    Hybrid retrieval combining FTS + semantic ranking
    
    Args:
        question (str): User question
        fts_limit (int): Number of chunks to retrieve from PostgreSQL FTS
        top_k_semantic (int): Number of top chunks to return after semantic ranking
    
    Returns:
        list: Top ranked chunks with chunk_id, document, semantic_score
    """
    
    # Step 1: Get top chunk IDs from PostgreSQL using keyword/question matching
    print(f"🔍 Step 1: Searching PostgreSQL for '{question}'...")
    chunk_ids = search_metadata(question, top_k=fts_limit)
    
    if not chunk_ids:
        print("❌ No matches found in PostgreSQL")
        return []
    
    print(f"✅ Found {len(chunk_ids)} chunks in PostgreSQL")
    
    # Step 2: Check which chunks exist in Chroma
    all_chroma_ids = set(collection.get(include=[])["ids"])
    available_ids = [cid for cid in chunk_ids if cid in all_chroma_ids]
    
    if not available_ids:
        print("❌ None of the chunks found in Chroma")
        return []
    
    print(f"✅ {len(available_ids)} chunks available in Chroma")
    
    # Step 3: Fetch chunks from Chroma with embeddings
    print("📦 Fetching chunks from Chroma...")
    chroma_results = collection.get(
        ids=available_ids,
        include=["documents", "embeddings", "metadatas"]
    )
    
    if not chroma_results or len(chroma_results["ids"]) == 0:
        print("❌ Failed to fetch chunks from Chroma")
        return []
    
    print(f"✅ Fetched {len(chroma_results['ids'])} chunks from Chroma")
    
    # Step 4: Semantic ranking
    print(f"🎯 Semantic ranking to get top {top_k_semantic}...")
    ranked_results = semantic_rank(question, chroma_results, top_k=top_k_semantic)
    
    if not ranked_results:
        print("❌ No semantic ranking results")
        return []
    
    print(f"✅ Retrieved {len(ranked_results)} top-ranked chunks")
    
    return ranked_results
