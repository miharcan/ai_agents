from pathlib import Path
from llama_index.core import Document

from llama_index.core import VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from sources.openstack.ingest import load_log_file
from sources.openstack.normalize import normalize_line
from sources.openstack.segment import build_service_segment
from sources.openstack.narrate import generate_service_narrative


def load_openstack_retriever(path: str):
    """
    Load OpenStack runtime logs (file or directory),
    build a narrated document, and return a retriever.
    """

    embed_model = HuggingFaceEmbedding(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    path = Path(path)
    lines: list[str] = []

    # --- Load logs ---
    if path.is_dir():
        for log_file in sorted(path.glob("*.log")):
            lines.extend(load_log_file(str(log_file)))
    else:
        lines = load_log_file(str(path))

    # --- Normalize ---
    events = [e for line in lines if (e := normalize_line(line))]

    # --- Segment (service-level, coarse) ---
    segment = build_service_segment(events)

    # --- Narrate ---
    narrative = generate_service_narrative(segment)

    documents = [
        Document(
            text=narrative,
            metadata={
                "source": "openstack",
                "type": "runtime",
            },
        )
    ]

    # --- Build index ---
    index = VectorStoreIndex.from_documents(
        documents,
        embed_model=embed_model,
    )

    return index.as_retriever(similarity_top_k=5)
