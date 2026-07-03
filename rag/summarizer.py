# 1. Import the modern client instead of the legacy 'model'
from rag.llm import client

def summarize_document(text):

    prompt = f"""
Provide a comprehensive, clear, and well-structured summary of the following document. 
Highlight the main themes, overall purpose, and core message.

Document:
{text[:12000]}
"""

    # 2. Update to use the modern SDK syntax
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text