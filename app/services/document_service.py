import os

from app.loaders.txt_loader import load_txt
from app.loaders.pdf_loader import load_pdf
from app.loaders.docx_loader import load_docx

def extract_text(file_path: str):

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".txt":
        return load_txt(file_path)

    elif extension == ".pdf":
        return load_pdf(file_path)
    
    elif extension == ".docx":
        return load_docx(file_path)

    raise ValueError(
        f"Unsupported file type: {extension}"
    )