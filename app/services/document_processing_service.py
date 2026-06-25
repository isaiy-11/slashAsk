import os

from app.services.document_service import extract_text
from app.services.chunking_service import create_chunks
from app.services.embedding_service import create_embeddings

from app.database.faiss_service import create_faiss_index
from app.database.faiss_service import save_index
from app.database.faiss_service import load_index
from app.database.faiss_service import add_embeddings_to_index

from app.services.storage_service import save_chunks
from app.services.storage_service import load_chunks
from app.services.storage_service import append_chunks


def process_document(file_path):

    text = extract_text(file_path)

    chunks = create_chunks(text)

    embeddings = create_embeddings(chunks)

    index = create_faiss_index(embeddings)

    index_path = "vector_store/indexes/master.index"

    chunk_path = "vector_store/chunks/master.pkl"

    if os.path.exists(index_path):

        existing_index = load_index(
        index_path
        )

        existing_index = add_embeddings_to_index(
        existing_index,
        embeddings
        )

        save_index(
        existing_index,
        index_path
        )

    else:

        index = create_faiss_index(
        embeddings
    )

    save_index(
        index,
        index_path
    )

    append_chunks(
    chunks,
    chunk_path
)
    return {
        "chunks_created": len(chunks),
        "index_saved": index_path,
        "chunk_file": chunk_path
     }