from typing import Literal
from .openai_runtime import run_openai
from .local_runtime import run_local

LLMBackend = Literal["openai", "local"]


def run_llm(prompt: str, backend: LLMBackend = "openai") -> str:
    if backend == "openai":
        print("LLM backend: OpenAI")
        return run_openai(prompt)

    elif backend == "local":
        print("LLM backend: Local (Ollama)")
        return run_local(prompt)

    else:
        raise ValueError(f"Unknown LLM backend: {backend}")
