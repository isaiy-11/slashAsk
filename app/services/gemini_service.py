import os
import google.generativeai as genai

from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def generate_answer(question, context):

    prompt = f"""
Answer the question using ONLY the provided context.

Context:
{context}

Question:
{question}

If the answer is not present in the context, say:
'The answer was not found in the uploaded document.'
"""

    response = model.generate_content(
        prompt
    )

    return response.text