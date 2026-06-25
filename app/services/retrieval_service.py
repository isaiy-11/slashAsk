import numpy as np

from app.database.faiss_service import load_index
from app.database.faiss_service import search_index

from app.services.storage_service import load_chunks
from app.services.embedding_service import model


def retrieve_chunks(
    question,
    index_path,
    chunk_path
):

    index = load_index(index_path)

    chunks = load_chunks(chunk_path)

    query_embedding = model.encode(
        [question]
    )

    query_embedding = np.array(
        query_embedding,
        dtype=np.float32
    )

    indices = search_index(
        index,
        query_embedding,
        top_k=20
    )

    results = []

    for idx in indices[0]:

        if idx < len(chunks):
            results.append(chunks[idx])

    # Debug: Print retrieved chunks
    # (Removed to avoid UnicodeEncodeError on Windows console)

    return results