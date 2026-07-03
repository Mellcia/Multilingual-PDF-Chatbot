# 1. Import the modern client instead of the legacy 'model'
from rag.llm import client

def general_chat(question):

    prompt = f"""
You are a helpful multilingual AI assistant.

Respond naturally to the user.

User:
{question}
"""

    try:
        # 2. Update to use the modern SDK syntax
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception:
        return (
            "⚠ Gemini API quota exceeded. "
            "Please try again later."
        )