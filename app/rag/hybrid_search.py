from rank_bm25 import BM25Okapi

def bm25_search(chunks, query, top_k=3):

    tokenized_chunks = [
        chunk.split()
        for chunk in chunks
    ]

    bm25 = BM25Okapi(tokenized_chunks)

    tokenized_query = query.split()

    scores = bm25.get_scores(tokenized_query)

    ranked = sorted(
        zip(chunks, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return ranked[:top_k]