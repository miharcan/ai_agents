from typing import Literal
from .openai_runtime import run_openai
from .local_runtime import run_local

LLMBackend = Literal["openai", "local"]


def run_llm(prompt: str, backend: str = "openai") -> str:
    if backend == "openai":
        print("LLM backend: OpenAI")
        return run_openai(prompt)

    elif backend in {"tiny", "mistral", "llama3", "phi3"}:
        print(f"LLM backend: Local {backend} (Ollama)")
        return run_local(prompt, backend)

    else:
        raise ValueError(f"Unknown LLM backend: {backend}")
