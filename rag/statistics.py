def get_document_statistics(
        text,
        pages
):

    words = len(text.split())

    characters = len(text)

    lines = len(
        text.splitlines()
    )

    return {
        "pages": pages,
        "words": words,
        "characters": characters,
        "lines": lines
    }