# 1. Import the modern client instead of the legacy 'model'
from rag.llm import client

def generate_key_points(text):

    prompt = f"""
Extract the important points from this document.

Return:
• Bullet points
• Important concepts
• Important definitions

Document:
{text[:12000]}
"""

    # 2. Update to use the modern SDK syntax
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text