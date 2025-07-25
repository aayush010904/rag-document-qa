import os
import tempfile
import requests
import asyncio
from typing import List
from urllib.parse import urlparse
from document_processor import extract_text_from_document, chunk_text
from vector_store import embed_and_store_chunks
from llm_client import ask_question


def get_file_extension_from_url(url: str) -> str:
    """Extract file extension from URL."""
    parsed = urlparse(url)
    path = parsed.path.lower()

   
    if ".pdf" in path:
        return ".pdf"
    elif ".docx" in path:
        return ".docx"
    elif ".doc" in path:
        return ".docx"  # Treat .doc as .docx
    elif ".eml" in path:
        return ".eml"
    elif ".msg" in path:
        return ".eml"  # Treat .msg as email
    else:
        # Default to PDF if unclear
        return ".pdf"


async def process_document_and_answer(blob_url: str, questions: List[str]) -> List[str]:
    # Download document
    response = requests.get(blob_url)
    if response.status_code != 200:
        raise Exception(
            f"Failed to download document from blob URL. Status: {response.status_code}"
        )

    # Determine file type and create temporary file
    file_extension = get_file_extension_from_url(blob_url)

    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp:
        tmp.write(response.content)
        tmp_path = tmp.name

    try:
        # Process document based on type
        text = extract_text_from_document(tmp_path)

        if not text.strip():
            raise Exception("No text could be extracted from the document")

        chunks = chunk_text(text)

        if not chunks:
            raise Exception("No chunks created from document text")

        embed_and_store_chunks(chunks)

        # Answer questions
        tasks = [ask_question(q) for q in questions]
        answers = await asyncio.gather(*tasks)

        return answers

    finally:
        # Clean up temporary file
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
