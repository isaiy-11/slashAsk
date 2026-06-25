from app.loaders.url_loader import extract_url_text

from app.services.chunking_service import create_chunks
from app.services.embedding_service import create_embeddings

from app.database.faiss_service import (
    load_index,
    save_index,
    add_embeddings_to_index,
    create_faiss_index
)

from app.services.storage_service import (
    append_chunks
)

import os


def process_url(url):

    text = extract_url_text(url)

    chunks = create_chunks(text)

    embeddings = create_embeddings(chunks)

    index_path = "vector_store/indexes/master.index"

    chunk_path = "vector_store/chunks/master.pkl"

    if os.path.exists(index_path):

        index = load_index(index_path)

        index = add_embeddings_to_index(
            index,
            embeddings
        )

        save_index(index, index_path)

    else:

        index = create_faiss_index(
            embeddings
        )

        save_index(index, index_path)

    append_chunks(
        chunks,
        chunk_path
    )

    return {
        "url": url,
        "chunks_added": len(chunks)
    }