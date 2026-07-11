from pypdf import PdfReader
from docx import Document
from bs4 import BeautifulSoup
import requests


def parse_pdf(file_path: str) -> str:
    """Extracts raw text from a PDF file, page by page."""
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text.strip()


def parse_docx(file_path: str) -> str:
    """Extracts raw text from a DOCX file, paragraph by paragraph."""
    doc = Document(file_path)
    text = "\n".join(para.text for para in doc.paragraphs if para.text.strip())
    return text.strip()


def parse_txt(file_path: str) -> str:
    """Reads plain text file content directly."""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read().strip()


def parse_url(url: str) -> str:
    """Fetches a web page and extracts visible text, stripping scripts/styles."""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ContextFlowAI/1.0"}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)


def parse_document(file_path: str, file_type: str) -> str:
    """
    Routes to the correct parser based on file_type.
    file_type: 'pdf', 'docx', 'txt', or 'url'
    For 'url', file_path should actually be the URL string.
    """
    if file_type == "pdf":
        return parse_pdf(file_path)
    elif file_type == "docx":
        return parse_docx(file_path)
    elif file_type == "txt":
        return parse_txt(file_path)
    elif file_type == "url":
        return parse_url(file_path)
    else:
        raise ValueError(f"Unsupported file_type: {file_type}")