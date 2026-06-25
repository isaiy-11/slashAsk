def create_chunks(
    text: str,
    chunk_size: int = 1500,
    overlap: int = 250
):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks