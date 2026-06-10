
from fastapi import APIRouter
from app.models.question_model import QuestionRequest
from app.services.chunking_service import create_chunks
from app.services.embedding_service import create_embeddings
from app.database.faiss_service import create_faiss_index
from app.services.embedding_service import create_embeddings
from app.services.retrieval_service import retrieve_chunks
from app.models.question_model import QuestionRequest
from app.services.rag_service import ask_document

router = APIRouter()

@router.post("/ask")
async def ask_question(request: QuestionRequest):

    return {
        "question_received": request.question,
        "answer": f"You asked: {request.question}"
    }
@router.get("/test-chunks")
async def test_chunks():

    sample_text = """
    FastAPI is a modern web framework.

    FAISS is used for vector search.

    RAG stands for Retrieval Augmented Generation.
    """

    chunks = create_chunks(
        sample_text,
        chunk_size=30
    )

    return {
        "total_chunks": len(chunks),
        "chunks": chunks
    }
@router.get("/test-embeddings")
async def test_embeddings():

    sample_chunks = [
        "FastAPI is a Python framework",
        "FAISS is a vector database",
        "RAG uses retrieval"
    ]

    embeddings = create_embeddings(
        sample_chunks
    )

    return {
        "total_chunks": len(sample_chunks),
        "embedding_dimension": len(embeddings[0])
    }
@router.get("/test-faiss")
async def test_faiss():

    chunks = [
        "FastAPI is a Python framework",
        "FAISS is used for vector search",
        "RAG uses retrieval"
    ]

    embeddings = create_embeddings(
        chunks
    )

    index = create_faiss_index(
        embeddings
    )

    return {
        "total_vectors": index.ntotal
    }
@router.get("/test-search")
async def test_search():

    results = retrieve_chunks(
        question="What is FastAPI?",
        index_path="vector_store/indexes/sample.txt.index",
        chunk_path="vector_store/chunks/sample.txt.pkl"
    )

    return {
        "retrieved_chunks": results
    }
@router.post("/ask-document")
async def ask_document_api(request: QuestionRequest):
   
    index_path = (
        f"vector_store/indexes/"
        f"{request.document_name}.index"
    )

    chunk_path = (
        f"vector_store/chunks/"
        f"{request.document_name}.pkl"
    )

    answer = ask_document(
        request.question,
        index_path,
        chunk_path,
        request.session_id
    )

    return {
        "document": request.document_name,
        "question": request.question,
        "answer": answer
    }
@router.get("/test-search")
async def test_search():

    results = retrieve_chunks(
        question="What is FAISS?",
        index_path="vector_store/indexes/sample.txt.index",
        chunk_path="vector_store/chunks/sample.txt.pkl"
    )

    return {
        "retrieved_chunks": results
    }
