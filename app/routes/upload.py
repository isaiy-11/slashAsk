import os

from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File

from app.services.document_processing_service import process_document

router = APIRouter()


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    upload_folder = "uploads"

    file_path = os.path.join(
        upload_folder,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    result = process_document(file_path)

    return {
    "message": "Document processed successfully",
    "filename": file.filename,
    "details": result
}

