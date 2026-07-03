from rag.preprocessing import clean_text
from rag.chunking import create_chunks
from rag.embeddings import generate_embeddings
from rag.vector_store import add_documents

def index_document(pages_text, filename, chat_id):
    all_chunks = []
    ids = []
    metadatas = []

    global_chunk_id = 0

    for page in pages_text:
        page_number = page["page"]
        
        # NOTE: If your queries are failing, ensure clean_text isn't 
        # accidentally destroying formatting or key marketing terminology.
        text = clean_text(page["text"])

        # Skip empty pages
        if not text or not text.strip():
            continue

        chunks = create_chunks(text)

        for i, chunk in enumerate(chunks):
            # Ensure the text chunk is not empty before indexing
            if not chunk.strip():
                continue
                
            all_chunks.append(chunk)

            # FIX: Scope the ID to include chat_id to ensure absolute uniqueness 
            # across the entire persistent database volume
            ids.append(f"{chat_id}_{filename}_{global_chunk_id}")

            metadatas.append(
                {
                    "file": filename,
                    "page": page_number,
                    "chunk": i
                }
            )

            global_chunk_id += 1

    # No valid chunks found to index
    if len(all_chunks) == 0:
        return 0

    # Generate high-dimensional embeddings for the text fragments
    embeddings = generate_embeddings(all_chunks)

    # Push chunks and vectors safely to the sandboxed database collection
    add_documents(
        chat_id,
        ids,
        all_chunks,
        embeddings,
        metadatas
    )

    return len(all_chunks)