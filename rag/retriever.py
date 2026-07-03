from rag.vector_store import client
from rag.embeddings import (
    generate_query_embedding
)

from rag.vector_store import (
    get_collection
)

def retrieve_chunks(
        question,
        chat_id,
        n_results=8
):
    collection = get_collection(
        chat_id
    )

    query_embedding = (
        generate_query_embedding(
            question
        )
    )

    # Convert embedding to clean native python numeric lists
    query_list = query_embedding.tolist()

    # Absolute dimensions safeguard alignment: 
    # Chroma DB requires query_embeddings to be passed strictly as [[vec1_float, vec2_float, ...]]
    if len(query_list) > 0 and not isinstance(query_list[0], list):
        query_list = [query_list]

    results = collection.query(
        query_embeddings=query_list,
        n_results=n_results
    )

    return results