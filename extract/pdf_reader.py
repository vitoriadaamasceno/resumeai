from PyPDF2 import PdfReader
from io import BytesIO


def get_pdf_text(pdf):

    pdf_reader = PdfReader(BytesIO(pdf))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text