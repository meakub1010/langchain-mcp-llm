from pydantic import BaseModel, Field
from app.model_factory import get_chat_model
from mcp_server.db import insert_review

class ExtractedReview(BaseModel):
    product_name: str | None = Field(None, description="Product mentioned, if any")
    order_id: int | None = Field(None, description="Order mentioned, if any")
    rating: int | None = Field(None, description="Rating out of 5, if mentioned or implied")
    mentions_shipping_issue: bool = Field(False, description="True if shipping delay/issue is mentioned")
    summary: str = Field(None, description="One-sentence summary of the feedback")

def extract_review(text: str):
    model = get_chat_model().with_structured_output(ExtractedReview)
    return model.invoke(
        f"Extract structured review information from this customer feedback: \n\n{text}"
    )

def extract_to_db(source_file: str, text: str) -> dict:
    try:
        review = extract_review(text)
    except Exception as e:
        return {"source_file": source_file, "inserted": False, "error": f"extraction failed: {e}"}

    try:
        review_id = insert_review(source_file, text, review)
    except Exception as e:
        return {"source_file": source_file, "inserted": False, "error": f"extraction failed: {e}"}

    return {"source_file": source_file, "inserted": True, "review_id": review_id}