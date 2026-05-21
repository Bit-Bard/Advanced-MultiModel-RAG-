def generate_citations(contexts):

    citations = []

    for ctx in contexts:

        metadata = ctx["metadata"]

        citation = (
            f"📄 {metadata['source']} "
            f"| Chunk: {metadata['chunk_id']}"
        )

        citations.append(citation)

    return list(set(citations))