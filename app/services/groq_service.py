import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_answer(
    question,
    context,
    history
):

    messages = [
        {
            "role": "system",
            "content": f"""
You are slashAsk, a helpful AI document assistant.

Answer questions using the provided document context.

Document Context:
{context}

If the answer is not available in the context,
say:

'Answer not found in the uploaded document.'

Provide clear and user-friendly responses.
"""
        }
    ]

    # Previous conversation history
    messages.extend(history)

    # Current user question
    messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )

    return response.choices[0].message.content