from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_text(text, source_name="unknown_file"):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    raw_chunks = splitter.split_text(text)

    chunks = []

    for i, chunk in enumerate(raw_chunks):

        chunks.append({
            "chunk": chunk,
            "metadata": {
                "source": source_name,
                "chunk_id": i,
                "type": "text"
            }
        })

    return chunks