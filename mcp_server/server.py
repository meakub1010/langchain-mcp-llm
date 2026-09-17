from mcp.server.fastmcp import FastMCP
from mcp_server.tools.query_database import query_database as _query_database
from mcp_server.tools.search_documents import search_documents as _search_documents
from mcp_server.tools.extract_to_db import extract_to_db as _extract_to_db

mcp = FastMCP("langchain-mcp-llm")


@mcp.tool()
def query_database(question: str) -> dict:
    return _query_database(question)

@mcp.tool()
def search_documents(query: str, top_k: int = 5) -> dict:
    """Find documents chunk related to natural language query, for answering questions from ingested files."""
    return _search_documents(query, top_k)

@mcp.tool()
def extract_to_db(source_file: str, text: str) -> dict:
    """"""
    return _extract_to_db(source_file, text)


if __name__ == "__main__":
    mcp.run(transport="stdio")


# test running mcp server using below command
# uv run python -m mcp_server.server