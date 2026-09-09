from app.model_factory import get_chat_model
from mcp_server.db import get_schema_description, run_readonly_query

SQL_SYSTEM_PROMPT = """You are a PostgreSQL expert. Given a database schema and a
question, write ONE read-only SQL query (SELECT or WITH only) that answers it.

Schema:
{schema}

Rules:
- Output ONLY the SQL query, no explanation, no markdown code fences.
- Never write INSERT/UPDATE/DELETE/DROP/ALTER — this connection can't run them anyway.
- Prefer explicit column names over SELECT *.
- The `orders.status` column is the current state of an order (pending/paid/shipped/
  delivered/cancelled). The `orders.shipped_at` column is non-null for any order that
  has EVER been shipped, including ones now delivered. If a question asks about orders
  "in shipped status" specifically, filter on status = 'shipped'. If it asks how many
  orders "have shipped" / "were shipped" in a general sense, filter on
  shipped_at IS NOT NULL.
"""

ANSWER_SYSTEM_PROMPT = """You answer questions using SQL query results.
Given the original question and the resulting rows, give a short, plain-English
answer. Mention specific numbers from the data. Do not mention SQL or tables."""

def query_database(question: str) -> dict:
    """Answers a natural-language question by generating and running SQL
        against the e-commerce database, then summarizing the result."""
    model = get_chat_model()
    schema = get_schema_description()
    sql_prompt = SQL_SYSTEM_PROMPT.format(schema=schema)
    sql_response = model.invoke([
        ("system", sql_prompt),
        ("user", question),
    ])

    sql = sql_response.content.strip().strip("`").removeprefix("sql").strip()
    rows = run_readonly_query(sql)

    answer_response = model.invoke([
        ("system", ANSWER_SYSTEM_PROMPT),
        ("user", f"Question: {question}\n\nResult rows: {rows}"),
    ])

    return {
        "answer": answer_response.content.strip().strip("`"),
        "sql": sql,
        "row_count": len(rows),
    }