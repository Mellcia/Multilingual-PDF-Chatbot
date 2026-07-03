import pdfplumber


def extract_text_pdf(pdf_path):

    text = ""
    page_data = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            for page in pdf.pages:

                page_text = page.extract_text()

                # Handle pages with no text
                if page_text is None:
                    page_text = ""

                # Store full document text
                if page_text.strip():
                    text += page_text + "\n"

                # Store page-wise data for citations
                page_data.append(
                    {
                        "page": page.page_number,
                        "text": page_text
                    }
                )
            return text, page_data, total_pages
    except Exception as e:

        print(
            f"Error reading PDF: {e}"
        )

        return (
            "",
            [],
            0
        )