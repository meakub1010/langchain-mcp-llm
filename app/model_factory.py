import os
from dotenv import load_dotenv
from langchain_core.language_models import BaseChatModel


load_dotenv()

def get_chat_model() -> BaseChatModel:
    provider = os.environ.get("LLM_PROVIDER", "anthropic").lower()

    if provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(
            model=os.environ["ANTHROPIC_MODEL"],
            api_key=os.environ["ANTHROPIC_API_KEY"],
        )
    if provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=os.environ["OPENAI_MODEL"],
            api_key=os.environ["OPENAI_API_KEY"],
        )

    raise ValueError(f"Unknown LLM provider: {provider!r}") # !r force string into re-presentation format