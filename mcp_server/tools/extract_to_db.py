from pydantic import BaseModel, Field
from app.model_factory import get_chat_model

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

# Test this without DB yet
# from mcp_server.tools.extract_to_db import extract_review
#
# result = extract_review("""
# Subject: Order #1042 - not happy
# The wireless mouse I got is fine but shipping took way too long,
# almost two weeks. Would give it 2 out of 5 stars overall.
# """)
# print(result)