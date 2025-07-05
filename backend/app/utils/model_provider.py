# app/utils/model_provider.py

from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel
from app.models.gemini_model import GeminiChatModel
import os

def get_model(provider: str, model_name: str = "", api_key: str = ""):
    provider = provider.lower()

    if provider == "anthropic":
        from anthropic import AsyncAnthropic
        client = AsyncAnthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
        return OpenAIChatCompletionsModel(model=model_name or "claude-3-opus", openai_client=client)

    elif provider == "google":
        return GeminiChatModel(model_name=model_name or "gemini-pro", api_key=api_key or os.getenv("GOOGLE_API_KEY"))

    else:
        client = AsyncOpenAI(
            base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
            api_key=api_key or os.getenv("OPENAI_API_KEY")
        )
        return OpenAIChatCompletionsModel(model=model_name or "gpt-4", openai_client=client)
