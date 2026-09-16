import psycopg

from mcp_server.db import get_connection, DATABASE_URL
from mcp_server.tools.extract_to_db import extract_review, extract_to_db


def test_extract_review_basic():
    result = extract_review("""
        Subject: Order #1042 - not happy
        The wireless mouse I got is fine but shipping took way too long,
        almost two weeks. Would give it 2 out of 5 stars overall.
        """)

    assert result.order_id == 1042
    assert result.rating == 2
    assert result.mentions_shipping_issue is True
    assert result.summary # non-empty


def test_extract_to_db_inserts_row():
    text = """
    Subject: Order #12 - not happy
    The wireless mouse I got is fine but shipping took way too long,
    almost two weeks. Would give it 2 out of 5 stars overall.
    """
    result = extract_to_db("test_review.txt", text)
    review_id = result["review_id"]
    try:
        assert result["inserted"] is True, result

        with get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM product_reviews WHERE id = %(id)s",
                {"id": result["review_id"]},
            ).fetchone()

        assert row is not None
        assert row["order_id"] == 12
        assert row["rating"] == 2
        assert row["mentions_shipping_issue"] is True
    finally:
        if review_id is not None:
            with psycopg.connect(DATABASE_URL) as clean_conn:
                clean_conn.execute(
                    "DELETE FROM product_reviews WHERE id = %(review_id)s",
                    {"review_id": review_id}
                )
                clean_conn.commit()