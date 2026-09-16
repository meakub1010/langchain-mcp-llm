from mcp_server.tools.extract_to_db import extract_review

result = extract_review("""
Subject: Order #1042 - not happy
The wireless mouse I got is fine but shipping took way too long,
almost two weeks. Would give it 2 out of 5 stars overall.
""")
print(result)


# run this
# uv run python scripts/test_extract.py