from llama_index.core import VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from rag.arxiv_loader import load_arxiv_documents


def load_docs(_ignored_path=None):
    """
    Build a retriever over arXiv abstracts.
    """

    embed_model = HuggingFaceEmbedding(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    docs = load_arxiv_documents(
        "../../datasets/archive/arxiv-metadata-oai-snapshot.json",
        limit=2000,   # keep demo fast & sane
    )

    index = VectorStoreIndex.from_documents(
        docs,
        embed_model=embed_model,
    )

    return index.as_retriever(similarity_top_k=5)
