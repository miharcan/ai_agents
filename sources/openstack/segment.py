def build_service_segment(events: list[str], max_lines: int = 300) -> list[str]:
    """
    Build a coarse-grained OpenStack service segment.
    """
    return events[:max_lines]
