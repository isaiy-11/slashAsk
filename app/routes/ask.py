
from fastapi import APIRouter
from app.models.question_model import QuestionRequest
from app.services.chunking_service import create_chunks
from app.services.embedding_service import create_embeddings
from app.database.faiss_service import create_faiss_index
from app.services.embedding_service import create_embeddings
from app.services.retrieval_service import retrieve_chunks
from app.models.question_model import QuestionRequest
from app.services.rag_service import ask_document
from app.services.session_service import get_history

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

    try:
        answer = ask_document(
            request.question,
            "vector_store/indexes/master.index",
            "vector_store/chunks/master.pkl",
            request.session_id
        )

        return {
            "question": request.question,
            "answer": answer
        }

    except Exception as e:
        return {
            "error": str(e)
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

@router.get("/history/{session_id}")
async def get_chat_history(session_id: str):
    try:
        raw_history = get_history(session_id)
        
        # Convert raw history list of dicts to the question-answer pair format expected by the UI
        formatted_history = []
        current_pair = {}
        for msg in raw_history:
            role = msg.get("role")
            content = msg.get("content")
            if role == "user":
                current_pair["question"] = content
            elif role == "assistant":
                current_pair["answer"] = content
                if "question" in current_pair:
                    formatted_history.append(current_pair)
                    current_pair = {}
                    
        return {
            "session_id": session_id,
            "history": formatted_history
        }
    except Exception as e:
        return {
            "error": str(e)
        }
