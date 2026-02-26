import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from .embedding import generate_embedding

def semantic_rank(user_query, chroma_results, top_k=3):
    """
    Performs semantic similarity ranking on FTS-filtered chunks.
    Returns top_k documents with chunk_id and similarity score.
    """

    # 1️⃣ Safety check
    if (
        chroma_results is None
        or "embeddings" not in chroma_results
        or len(chroma_results["embeddings"]) == 0
    ):
        return []

    # 2️⃣ Embed user query
    query_embedding = np.array(generate_embedding(user_query)).reshape(1, -1)

    # 3️⃣ Convert chunk embeddings to np.array
    chunk_embeddings = np.array(chroma_results["embeddings"])
    if chunk_embeddings.size == 0:
        return []

    # 4️⃣ Compute cosine similarity
    similarities = cosine_similarity(query_embedding, chunk_embeddings)[0]

    # 5️⃣ Sort by highest similarity
    sorted_indices = np.argsort(similarities)[::-1]

    # 6️⃣ Build ranked results
    ranked_results = []
    for idx in sorted_indices[:top_k]:
        ranked_results.append({
            "chunk_id": chroma_results["ids"][idx],
            "document": chroma_results["documents"][idx],
            "semantic_score": float(round(similarities[idx], 4))
        })

    return ranked_results
