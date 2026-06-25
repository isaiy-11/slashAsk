import os

from fastapi import FastAPI
from app.routes.ask import router as ask_router
from app.routes.upload import router as upload_router
from app.routes.document import router as document_router
from app.routes.url import router as url_router

# Ensure required storage directories exist before handling requests
for _folder in (
    "uploads",
    "vector_store/indexes",
    "vector_store/chunks",
):
    os.makedirs(_folder, exist_ok=True)

app = FastAPI()
app.include_router(upload_router)
app.include_router(ask_router)
app.include_router(document_router)
app.include_router(url_router)

@app.get("/")
async def root():
    return {"message": "Multi Document QA Bot Running"}