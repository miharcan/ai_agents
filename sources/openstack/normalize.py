def normalize_line(line: str) -> str | None:
    # For now, pass through non-empty lines
    return line.strip() if line.strip() else None
