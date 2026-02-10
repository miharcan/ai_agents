import subprocess

OLLAMA_MODEL_MAP = {
    "tiny": "phi3:mini",
    "mistral": "mistral",
    "llama3": "llama3:8b",
    "phi3": "phi3:medium",
    "qwen14": "qwen2.5:14b",
}


def run_local(prompt: str, llm_name: str) -> str:
    model = OLLAMA_MODEL_MAP[llm_name]
    process = subprocess.run(
        ["ollama", "run", model],
        input=prompt,
        text=True,
        capture_output=True,
    )

    if process.returncode != 0:
        raise RuntimeError(
            f"Ollama failed:\n{process.stderr.strip()}"
        )

    output = process.stdout.strip()

    if not output:
        raise RuntimeError(
            "Ollama returned no output. "
            "Check that the model is installed and working:\n"
            "  ollama run mistral"
        )

    return output
