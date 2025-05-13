import pymupdf


def get_pdf_text(pdf):

    doc = pymupdf.open(pdf)
    text = ""
    for page in doc:
        text += page.get_text()
    return text