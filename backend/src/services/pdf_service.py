from io import BytesIO
from pypdf import PdfReader


async def extract_text(file_content: bytes):

    reader = PdfReader(BytesIO(file_content))

    pages = []

    for page in reader.pages:
        pages.append(page.extract_text() or "")

    return pages
