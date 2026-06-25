from fastapi import APIRouter
from pydantic import BaseModel

from app.services.url_processing_service import process_url

router = APIRouter()


class URLRequest(BaseModel):
    url: str


@router.post("/upload-url")
async def upload_url(
    request: URLRequest
):

    result = process_url(
        request.url
    )

    return result