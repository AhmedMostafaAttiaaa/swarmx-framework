from typing import Any
from .base import BaseLLM
from .ollama import OllamaLLM
from .groq import GroqLLM
from .gemini import GeminiLLM
from .openai import OpenAILLM

PROVIDERS = {"ollama": OllamaLLM, "groq": GroqLLM, "gemini": GeminiLLM, "openai": OpenAILLM}
def create_model(provider: str, model: str, **config: Any) -> BaseLLM:
    if not model:
        model = config.pop("default_model", None) or ""
    try: return PROVIDERS[provider.lower()](model, **config)
    except KeyError as e: raise ValueError(f"Unsupported provider: {provider}") from e
