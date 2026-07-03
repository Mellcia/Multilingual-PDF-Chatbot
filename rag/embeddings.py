from sentence_transformers import SentenceTransformer

_model = None

def get_model():
    global _model

    if _model is None:
        print("Loading embedding model...")
        _model = SentenceTransformer(
            "paraphrase-multilingual-MiniLM-L12-v2"
        )

    return _model


def generate_embeddings(chunks):
    model = get_model()

    return model.encode(
        chunks,
        convert_to_numpy=True
    )


def generate_query_embedding(question):
    model = get_model()
    
    # Absolute alignment safeguard: force string into a structured list block
    if isinstance(question, str):
        question = [question]

    return model.encode(
        question,
        convert_to_numpy=True
    )