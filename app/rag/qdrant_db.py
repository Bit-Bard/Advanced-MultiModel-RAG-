from qdrant_client import QdrantClient

client = QdrantClient(
    host="localhost",
    port=6333
)


from qdrant_client.models import (
    VectorParams,
    Distance
)

def create_collection():

    client.recreate_collection(
        collection_name="rag_collection",

        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    )

    print("Collection Created")


from qdrant_client.models import PointStruct

def upload_data(processed_data):

    points = []

    for idx, item in enumerate(processed_data):

        points.append(

            PointStruct(
                id=idx,

                vector=item["embedding"].tolist(),

                payload={
                    "chunk": item["chunk"],
                    "metadata": item["metadata"]
                }
            )
        )

    client.upsert(
        collection_name="rag_collection",
        points=points
    )

    print("Embeddings Uploaded")

    
from rag.embedder import model

def search_query(query, top_k=3):

    query_vector = model.encode(query).tolist()

    results = client.query_points(
        collection_name="rag_collection",
        query=query_vector,
        limit=top_k
    ).points

    return results


