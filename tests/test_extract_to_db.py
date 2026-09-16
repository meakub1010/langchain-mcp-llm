from mcp_server.tools.extract_to_db import extract_review

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