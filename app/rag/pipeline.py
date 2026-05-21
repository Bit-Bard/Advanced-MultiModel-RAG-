from rag.chunker import chunk_text
from rag.embedder import create_embeddings

def process_document(text, source_name):

    chunk_data = chunk_text(text, source_name)

    texts = [item["chunk"] for item in chunk_data]

    embeddings = create_embeddings(texts)

    processed_data = []

    for i, item in enumerate(chunk_data):

        processed_data.append({

            "chunk": item["chunk"],

            "embedding": embeddings[i],

            "metadata": item["metadata"]
        })

    return processed_data