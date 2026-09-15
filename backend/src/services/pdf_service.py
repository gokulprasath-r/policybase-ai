from pypdf import PdfReader

async def extract_text(file_path: str):
    reader = PdfReader(file_path)

    pages=[]

    for page in reader.pages:
        pages.append(page.extract_text())

    return pages
