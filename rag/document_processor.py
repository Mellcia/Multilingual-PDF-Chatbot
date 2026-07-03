import os
from rag.pdf_loader import extract_text_pdf
from rag.ocr import extract_scanned_pdf
from rag.preprocessing import is_scanned_pdf

def process_pdf(pdf_path, chat_id):
    """
    Processes the PDF file from the isolated chat folder and caches the 
    extracted text into a structured per-chat text folder.
    """
    scanned = is_scanned_pdf(pdf_path)

    if scanned:
        text, page_data, pages = (
            extract_scanned_pdf(pdf_path)
        )
        pdf_type = "Scanned PDF"
    else:
        text, page_data, pages = (
            extract_text_pdf(pdf_path)
        )
        pdf_type = "Text PDF"

    # Ensure the isolated workspace data and text cache folder exists
    filename = os.path.basename(pdf_path)
    base_name, _ = os.path.splitext(filename)
    
    text_cache_dir = os.path.join("workspace_data", chat_id, "text_cache")
    os.makedirs(text_cache_dir, exist_ok=True)
    
    # Save the extracted text locally inside the isolated chat cache
    txt_save_path = os.path.join(text_cache_dir, f"{base_name}.txt")
    with open(txt_save_path, "w", encoding="utf-8") as f:
        f.write(text)

    return {
        "pdf_type": pdf_type,
        "text": text,
        "pages": pages,

        # Existing key
        "page_data": page_data,

        # Added in Phase 6
        "pages_text": page_data
    }