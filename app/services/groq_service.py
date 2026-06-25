import os
from openai import AzureOpenAI

_client = None

def get_client():
    global _client
    if _client is None:
        _client = AzureOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", "https://trackerwaveaichat.openai.azure.com/"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY", ""),
            api_version="2024-02-01"
        )
    return _client


def generate_answer(
    question,
    context,
    history
):
    messages = [
        {
            "role": "system",
            "content": f"""
You are slashAsk, an intelligent AI assistant.

Your job is to answer questions using the provided document context and behave like a helpful chatbot.

DOCUMENT CONTEXT:
{context}

RULES:

1. Understand the document content and explain it naturally.
2. Do not copy chunks directly from the document.
3. Do not say:
   - "According to the document"
   - "The document mentions"
   - "Refer to section"
   - "See page"
4. If the answer contains steps, explain them clearly in numbered format.
5. Summarize technical content in simple language when possible.
6. Maintain a conversational chatbot style.
7. Use previous conversation history when relevant.
8. If the user's input is a broad topic (e.g., "asset tracking" or "asset management"), provide a comprehensive summary of everything the document says about that topic. 
9. If the context does not contain the answer, do your best to be helpful based on general knowledge and whatever context is available, but clarify what is and isn't from the document. Do not just reply "Answer not found".

Example:

Question:
How to assign token?

Bad Answer:
The document mentions Assign Token in section 2.1.

Good Answer:
To assign a token:

1. Open the application.
2. Navigate to the Assign Token section.
3. Select the patient.
4. Click Assign Token.
5. Confirm the assignment.

The token will now be linked to the selected patient.

Provide complete and helpful answers.
"""
        }
    ]

    messages.extend(history)

    messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    response = get_client().chat.completions.create(
        model="gpt-5.5",
        messages=messages
    )

    return response.choices[0].message.content