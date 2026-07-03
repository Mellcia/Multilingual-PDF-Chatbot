import chromadb
from chromadb.config import Settings

# Initialize the persistent local ChromaDB client
client = chromadb.PersistentClient(
    path="database/chroma_db"
)

def get_collection(chat_id):
    """
    Retrieves or creates a unique sandboxed collection for the active chat workspace.
    Uses cosine distance metric for reliable multilingual embedding lookups.
    """
    return client.get_or_create_collection(
        name=f"chat_{chat_id}",
        metadata={"hnsw:space": "cosine"}
    )

def add_documents(chat_id, ids, chunks, embeddings, metadatas):
    """
    Adds text fragments and their matching high-dimensional vector embeddings 
    to the per-chat sandboxed collection layer.
    """
    collection = get_collection(chat_id)

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )

def clear_vector_database(chat_id):
    """
    FIXED: Now takes chat_id as a parameter to clear out only the 
    ingested knowledge for the active workspace instead of targeting 'pdf_collection'.
    """
    try:
        client.delete_collection(name=f"chat_{chat_id}")
    except Exception:
        pass
    
    # Re-initialize an empty collection for the workspace right away
    _ = get_collection(chat_id)

def delete_chat_collection(chat_id):
    """
    Purges the entire workspace vector store layer from disk when a chat session is deleted.
    """
    try:
        client.delete_collection(name=f"chat_{chat_id}")
    except Exception:
        pass