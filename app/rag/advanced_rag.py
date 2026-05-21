from rag.query_rewriter import rewrite_query
from rag.qdrant_db import search_query
from rag.reranker import rerank

def advanced_retrieval(user_query):

    improved_query = rewrite_query(user_query)

    results = search_query(improved_query)

    retrieved = []

    for r in results:

        retrieved.append({
            "chunk": r.payload["chunk"],
            "metadata": r.payload["metadata"]
        })

    chunk_texts = [
        item["chunk"]
        for item in retrieved
    ]

    ranked = rerank(
        improved_query,
        chunk_texts
    )

    final_results = []

    for chunk, score in ranked[:2]:

        for item in retrieved:

            if item["chunk"] == chunk:

                final_results.append({
                    "chunk": chunk,
                    "score": float(score),
                    "metadata": item["metadata"]
                })

    return final_results