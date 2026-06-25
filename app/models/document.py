from pydantic import BaseModel
from datetime import datetime

class DocumentMeta(BaseModel):
    doc_id: str
    filename: str
    upload_time: datetime
    source_type: str  # "file" or "url"