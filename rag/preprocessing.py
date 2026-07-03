import pdfplumber
import re

def is_scanned_pdf(pdf_path):

    try:

        with pdfplumber.open(pdf_path) as pdf:

            page = pdf.pages[0]

            text = page.extract_text()

            if text and len(text.strip()) > 20:
                return False

            return True

    except:
        return True

def clean_text(text):

    if not text:
        return ""

    text = re.sub(r'\s+', ' ', text)

    text = text.replace('\x0c', '')

    return text.strip()