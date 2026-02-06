def load_log_file(path: str) -> list[str]:
    with open(path, "r", errors="ignore") as f:
        return [line.strip() for line in f if line.strip()]
