def generate_boot_narrative(segment: list[str]) -> str:
    """
    Generate a structured narrative from a Linux boot segment.

    This function does not judge correctness; it highlights
    potentially noteworthy signals for downstream reasoning.
    """

    lines = segment[:200]  # cap size for now
    text = "\n".join(lines).lower()

    observations = []

    # --- Lightweight signal detection ---
    if "acpi" in text and "disabled" in text:
        observations.append("ACPI appears to be disabled (legacy or firmware limitation).")

    if "apm" in text:
        observations.append("APM (legacy power management) is present.")

    if "selinux" in text:
        observations.append("SELinux security framework is enabled.")

    if "memory:" in text or "mem=" in text:
        observations.append("System memory information is present; system may be resource constrained.")

    if "i810" in text or "intel" in text:
        observations.append("Intel i810-era graphics hardware detected (very old chipset).")

    # --- Compose narrative ---
    narrative = [
        "Linux boot sequence summary:",
        "",
        "Observed signals:",
    ]

    if observations:
        for obs in observations:
            narrative.append(f"- {obs}")
    else:
        narrative.append("- No immediately notable signals detected.")

    narrative.extend([
        "",
        "Boot log excerpt:",
        "",
        *lines
    ])

    return "\n".join(narrative)
