import pypdf

__all__ = ["get_pdf_text"]


def get_pdf_text(pdf_file):
    reader = pypdf.PdfReader(pdf_file)

    text_pieces = []
    for page in reader.pages:
        text_pieces.append(page.extract_text())

    return " ".join(text_pieces)
