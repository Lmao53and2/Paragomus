from agno.document.reader.pdf_reader import PDFReader

def extract_text_from_pdf(file_path):
    reader = PDFReader()
    documents = reader.read(file_path)
    return "\n".join(doc.content for doc in documents if doc.content)
