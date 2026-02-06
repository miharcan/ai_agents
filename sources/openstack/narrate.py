def generate_service_narrative(segment: list[str]) -> str:
    """
    Generate a structured narrative from OpenStack service logs.

    Highlights operational signals without asserting root cause.
    """

    lines = segment[:300]
    text = "\n".join(lines).lower()

    observations = []

    # --- Lightweight signal detection ---
    if "error" in text or "exception" in text:
        observations.append("Error or exception messages are present in service logs.")

    if "timeout" in text:
        observations.append("Service timeouts detected (possible dependency or performance issues).")

    if "connection refused" in text or "failed to connect" in text:
        observations.append("Service connection failures observed.")

    if "retrying" in text or "retry" in text:
        observations.append("Retry behavior detected, indicating transient failures.")

    if "keystone" in text:
        observations.append("Keystone (identity service) activity present.")

    if "database" in text or "mysql" in text or "postgres" in text:
        observations.append("Database interactions detected (potential backend dependency).")

    if "rabbit" in text or "amqp" in text:
        observations.append("Message queue (RabbitMQ/AMQP) interactions detected.")

    # --- Compose narrative ---
    narrative = [
        "OpenStack service log summary:",
        "",
        "Observed signals:",
    ]

    if observations:
        for obs in observations:
            narrative.append(f"- {obs}")
    else:
        narrative.append("- No immediately notable service-level signals detected.")

    narrative.extend([
        "",
        "Service log excerpt:",
        "",
        *lines
    ])

    return "\n".join(narrative)
