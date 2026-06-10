from pydantic import BaseModel


class QuestionRequest(BaseModel):

    document_name: str
    question: str
    session_id: str