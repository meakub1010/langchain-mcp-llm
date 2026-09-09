import hashlib
from pathlib import Path

import psycopg
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

from mcp_server.db import upsert_chunk
from mcp_server.embeddings import embed_texts

_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100
)

def _read_file_text(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or " " for page in reader.pages)
    return path.read_text(encoding="utf-8", errors="ignore")

def ingest_files(file_paths: list[str]) -> dict:
    """

    :param file_paths:
    Chunks and embeds one or more local files (.txt, .md, .pdf) into document_chunks for later retrieval by search documents
    :return: dictionary of chunk and embeddings
    """
    files_processed, files_failed = 0, []
    chunks_written, chunks_skipped, chunks_failed = 0,0,[]

    for file_path in file_paths:
        path = Path(file_path)
        try:
            text = _read_file_text(path)
        except Exception as e:
            files_failed.append({"file": file_path, "error": str(e)})
            continue
        if not text.strip():
            files_failed.append({"file": file_path, "error": "no extractable text found"})
            continue
        source_id = path.name
        chunks = _splitter.split_text(text)
        embeddings = embed_texts(chunks)

        for chunk_text, embedding in zip(chunks, embeddings):
            content_hash = hashlib.sha256(chunk_text.encode("utf-8")).hexdigest()
            try:
                was_new = upsert_chunk(
                    source_id=source_id,
                    source_url=str(path),
                    content=chunk_text,
                    content_hash=content_hash,
                    embedding=embedding
                )

                if was_new:
                    chunks_written += 1
                else:
                    chunks_skipped += 1
            except psycopg.Error as e:
                files_failed.append({"file": file_path, "error": str(e)})

        files_processed += 1
    return {
        "files_processed": files_processed,
        "files_failed": files_failed,
        "chunks_written": chunks_written,
        "chunks_skipped": chunks_skipped,
        "chunks_failed": chunks_failed
    }


