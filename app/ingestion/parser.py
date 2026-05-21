import fitz

def extract_pdf_text(pdf_path):
    doc = fitz.open(pdf_path)

    full_text = ""

    for page_num, page in enumerate(doc):
        text = page.get_text()

        full_text += f"\n--- Page {page_num+1} ---\n"
        full_text += text

    return full_text


from docx import Document

def extract_docx_text(docx_path):

    doc = Document(docx_path)

    full_text = ""

    for para in doc.paragraphs:
        full_text += para.text + "\n"

    return full_text