from fastapi import APIRouter
import os

router = APIRouter()


@router.get("/documents")
async def list_documents():

    upload_folder = "uploads"

    documents = os.listdir(upload_folder)

    return {
        "total_documents": len(documents),
        "documents": documents
    }
@router.get("/document-details/{document_name}")
async def document_details(document_name: str):

    upload_path = f"uploads/{document_name}"

    index_path = (
        f"vector_store/indexes/{document_name}.index"
    )

    chunk_path = (
        f"vector_store/chunks/{document_name}.pkl"
    )

    if not os.path.exists(upload_path):

        return {
            "error": "Document not found"
        }

    file_size = os.path.getsize(upload_path)

    return {
        "document_name": document_name,
        "file_size_kb": round(file_size / 1024, 2),
        "index_exists": os.path.exists(index_path),
        "chunk_exists": os.path.exists(chunk_path)
    }
@router.delete("/document/{document_name}")
async def delete_document(document_name: str):

    upload_path = f"uploads/{document_name}"

    index_path = (
        f"vector_store/indexes/{document_name}.index"
    )

    chunk_path = (
        f"vector_store/chunks/{document_name}.pkl"
    )

    deleted_files = []

    if os.path.exists(upload_path):
        os.remove(upload_path)
        deleted_files.append(upload_path)

    if os.path.exists(index_path):
        os.remove(index_path)
        deleted_files.append(index_path)

    if os.path.exists(chunk_path):
        os.remove(chunk_path)
        deleted_files.append(chunk_path)

    return {
        "message": "Document deleted successfully",
        "deleted_files": deleted_files
    }