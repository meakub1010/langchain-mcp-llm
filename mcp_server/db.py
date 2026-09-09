import os
import re
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_URL_READONLY = os.getenv("DATABASE_URL_READONLY")

def get_connection():
    """Opens readonly connection to PostgreSQL database - will reject any insert update delete or ddl on this connection"""
    # row_factory=dict_row — this is the interesting part. By default, psycopg3 returns query rows as plain tuples:
    # (1, 'some text')
    # with row_dict # {'id': 1, 'content': 'some text'}
    return psycopg.connect(DATABASE_URL_READONLY, row_factory=dict_row)

def get_schema_description() -> str:
    """Returns schema description"""
    query = """
    SELECT table_name, column_name, data_type
    FROM information_schema.columns
    WHERE table_schema = 'public'
    ORDER BY table_schema, ordinal_position;
    """

    with get_connection() as conn:
        rows = conn.execute(query).fetchall()

    tables: dict[str, list[str]] = {}
    for row in rows:
        tables.setdefault(row["table_name"], []).append(
            f'{row["column_name"]} ({row["data_type"]})'
        )

    return "\n".join(
        f"{table}:{', '.join(columns)}"
        for table, columns in tables.items()
    )

_SELECT_ONLY = re.compile(r"^\s*(SELECT|WITH)\b", re.IGNORECASE)

def run_readonly_query(sql:str) -> list[dict]:
    if not _SELECT_ONLY.match(sql):
        raise ValueError(f"Only SELECT/WITH queries are allowed. Got: {sql[:80]!r}")

    with get_connection() as conn:
        return conn.execute(sql).fetchall()

def upsert_chunk(source_id: str, source_url: str | None, content: str, content_hash: str, embedding: list[float]) -> None:
    """insert chunk or does nothing is the exact (source_id, content_hash) already exist
    this is for incremental re-indexing
    """
    query = """
        INSERT INTO document_chunks(source_id, source_url, content, content_hash, embedding)
        VALUES (%(source_id)s, %(source_url)s, %(content)s, %(content_hash)s, %(embedding)s)
        ON CONFLICT (source_id, content_hash) DO NOTHING
        RETURNING id;
    """

    with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
        result = conn.execute(query, {
            "source_id": source_id,
            "source_url": source_url,
            "content": content,
            "content_hash": content_hash,
            "embedding": embedding,
        }).fetchone()
        conn.commit()

    return result is not None