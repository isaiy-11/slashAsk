from fastapi import FastAPI
from app.routes.ask import router as ask_router
from app.routes.upload import router as upload_router
from app.routes.document import router as document_router

app = FastAPI()
app.include_router(upload_router)
app.include_router(ask_router)
app.include_router(document_router)

@app.get("/")
async def root():
    return {"message": "Multi Document QA Bot Running"}
