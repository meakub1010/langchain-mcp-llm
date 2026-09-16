from mcp_server.db import search_chunks
from mcp_server.embeddings import embed_texts

def search_documents(query: str, top_k: int = 5) -> dict:
    """
    Find document chunks semantically similar to a natural-language query,
    for answering questions from ingested files.
    """
    [query_embedding] = embed_texts([query])

    try:
        results = search_chunks(query_embedding, top_k)
    except Exception as e:
        return {"query": query, "results": [], "error": str(e)}

    return {
        "query": query,
        "results": [
            {
                "source_d": r["source_id"],
                "source_url": r["source_url"],
                "content": r["content"],
                "similarity": round(r["similarity"], 4),

            }
            for r in results
        ],
    }