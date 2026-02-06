from llama_index.core import Document
from data.sources.linux.ingest import load_log_file
from data.sources.linux.normalize import normalize_line
from data.sources.linux.segment import build_boot_segment
from data.sources.linux.narrate import generate_boot_narrative


def load_linux_documents(log_path: str):
    lines = load_log_file(log_path)
    events = [e for line in lines if (e := normalize_line(line))]

    segment = build_boot_segment(events)
    narrative = generate_boot_narrative(segment)

    return [
        Document(
            text=narrative,
            metadata={
                "source": "linux",
                "type": "boot"
            }
        )
    ]
