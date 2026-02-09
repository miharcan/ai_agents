import subprocess
import os

model = os.environ.get("OLLAMA_MODEL", "llama3:8b")

def run_local(prompt: str) -> str:
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
