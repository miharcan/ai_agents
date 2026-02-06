from pathlib import Path

def load_log_file(path: str) -> list[str]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(path)

    with p.open("r", encoding="utf-8", errors="ignore") as f:
        return [line.rstrip("\n") for line in f]
