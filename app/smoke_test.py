
from app.model_factory import get_chat_model

if __name__ == "__main__":
    model = get_chat_model()
    response = model.invoke("Reply with exactly one sentence confirming you're working.")
    print(response.content)