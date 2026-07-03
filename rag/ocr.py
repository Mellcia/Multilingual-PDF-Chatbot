from pdf2image import convert_from_path
import pytesseract

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

def extract_scanned_pdf(pdf_path):

    images = convert_from_path(pdf_path)

    text = ""
    page_data = []

    for i, image in enumerate(images):

        page_text = pytesseract.image_to_string(
            image,
            lang="eng"
        )

        text += page_text + "\n"

        page_data.append(
            {
                "page": i + 1,
                "text": page_text
            }
        )

    return text, page_data, len(images)