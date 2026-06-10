import os

from app.services.document_service import extract_text
from app.services.chunking_service import create_chunks
from app.services.embedding_service import create_embeddings

from app.database.faiss_service import create_faiss_index
from app.database.faiss_service import save_index

from app.services.storage_service import save_chunks


def process_document(file_path):

    text = extract_text(file_path)

    chunks = create_chunks(text)

    embeddings = create_embeddings(chunks)

    index = create_faiss_index(embeddings)

    filename = os.path.basename(file_path)

    index_path = f"vector_store/indexes/{filename}.index"

    chunk_path = f"vector_store/chunks/{filename}.pkl"

    save_index(index, index_path)

    save_chunks(chunks, chunk_path)

    return {
        "chunks_created": len(chunks),
        "index_saved": index_path,
        "chunk_file": chunk_path
    }