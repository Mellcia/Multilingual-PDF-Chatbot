from langchain_text_splitters import RecursiveCharacterTextSplitter

def create_chunks(text):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=200,
        length_function=len
    )

    chunks = splitter.split_text(text)

    return chunks