from rag.retriever import retrieve_chunks
from rag.language_detector import detect_language
# 1. Import the modern client instead of the legacy 'model'
from rag.llm import client 
from rag.translator import translate_text
from rag.confidence import calculate_confidence
from rag.general_chat import general_chat

def answer_question(
        question,
        chat_id,
        chat_history=""
):
    # 1. Tukuyin ang eksaktong wika na ginamit ng user sa kanyang tanong
    language = detect_language(question)

    # Isalin sa English para sa internal processing ng RAG
    translated_question = translate_text(question, target="en")
    
    docs = []
    metas = []
    results = {}
    confidence = 0

    try:
        results = retrieve_chunks(translated_question, chat_id)
        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]
        
        if "distances" in results and results["distances"]:
            confidence = calculate_confidence(results["distances"][0])
    except Exception:
        answer = general_chat(translated_question)
        # Tiyakin na isasalin pabalik sa wika ng user ang sagot mula sa general chat
        if language and language != "en":
            answer = translate_text(answer, source="en", target=language)
        return (answer, [], 0)

    context = ""
    sources = []

    if docs and len(docs) > 0:
        for doc, meta in zip(docs, metas):
            if not doc or not meta:
                continue
            context += doc + "\n\n"
            source = f"{meta.get('file', 'Unknown')} | Page {meta.get('page', 'N/A')} | Chunk {meta.get('chunk', 'N/A')}"
            sources.append(source)
        sources = list(set(sources))

    prompt = f"""
You are a highly intelligent, natural, and helpful multilingual AI assistant.

Your goal is to answer the user's question, preferring the provided PDF context whenever possible.

Chat History:
{chat_history}

Question:
{translated_question}

PDF Context:
{context if context.strip() else "[No relevant text chunks found in the document for this specific question]"}

Instructions:
1. First, search the provided PDF Context thoroughly to see if it answers the question. If the answer is there, use it to form your response.
2. If the answer is NOT present in the PDF context, or if the user is asking a general question/greeting that wouldn't be in a document, do NOT say you can't find it. Simply switch over to your own general pre-trained knowledge and answer the user naturally, accurately, and conversationally.
3. Maintain a friendly and helpful tone. Do not use robotic disclaimers or mention that you are switching to general knowledge unless directly relevant to the user's request.
"""

    # 2. Modern SDK syntax implementation using the client object
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    answer = response.text

    # 2. MAHIGPIT NA LOGIC: Isalin pabalik ang sagot sa naitatalang wika ng user (language)
    if language and language != "en":
        answer = translate_text(answer, source="en", target=language)

    if not context.strip():
        sources = []

    return (answer, sources, confidence)