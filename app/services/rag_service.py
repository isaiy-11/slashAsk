from app.services.retrieval_service import retrieve_chunks
from app.services.groq_service import generate_answer

from app.services.session_service import (
    add_message,
    get_history
)


def ask_document(
    question,
    index_path,
    chunk_path,
    session_id
):

    question_lower = question.lower().strip()

    # =====================
    # General Chatbot Layer
    # =====================

    greetings = [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening"
    ]

    if question_lower in greetings:
        return (
            "Hello! 👋 I'm slashAsk. "
            "Ask me anything about your uploaded documents."
        )

    if "who are you" in question_lower:
        return (
            "I'm slashAsk 🤖, your AI-powered document assistant. "
            "I can answer questions from the documents you upload."
        )

    if "thank" in question_lower:
        return (
            "You're welcome! 😊 "
            "Feel free to ask more questions."
        )

    if "bye" in question_lower:
        return (
            "Goodbye! 👋 "
            "Have a great day."
        )

    # =====================
    # RAG Processing
    # =====================

    chunks = retrieve_chunks(
        question,
        index_path,
        chunk_path
    )

    context = "\n".join(chunks)

    # Get session history
    history = get_history(
        session_id
    )

    answer = generate_answer(
        question,
        context,
        history
    )

    # Save conversation
    add_message(
        session_id,
        "user",
        question
    )

    add_message(
        session_id,
        "assistant",
        answer
    )

    return answer