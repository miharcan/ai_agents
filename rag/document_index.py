from pathlib import Path
import faiss

from llama_index.core import (
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.faiss import FaissVectorStore

from .arxiv_loader import load_arxiv_documents

INDEX_DIR = Path("data/arxiv_index")
ARXIV_JSON = Path("../../datasets/archive/arxiv-metadata-oai-snapshot.json")

EMBED_DIM = 384


def load_docs():
    embed_model = HuggingFaceEmbedding(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    faiss_path = INDEX_DIR / "vector_store.faiss"

    if INDEX_DIR.exists() and faiss_path.exists():
        print("Loading cached arXiv index (FAISS)...")

        faiss_index = faiss.read_index(str(faiss_path))
        vector_store = FaissVectorStore(faiss_index=faiss_index)

        storage_context = StorageContext.from_defaults(
            vector_store=vector_store,
            persist_dir=INDEX_DIR,
        )

        index = load_index_from_storage(
            storage_context,
            embed_model=embed_model,
        )

    else:
        print("🔨 Building arXiv index (first run, this will take time)...")
        INDEX_DIR.mkdir(parents=True, exist_ok=True)

        docs = load_arxiv_documents(ARXIV_JSON)

        faiss_index = faiss.IndexFlatL2(EMBED_DIM)
        vector_store = FaissVectorStore(faiss_index=faiss_index)

        storage_context = StorageContext.from_defaults(
            vector_store=vector_store
        )

        index = VectorStoreIndex.from_documents(
            docs,
            storage_context=storage_context,
            embed_model=embed_model,
        )

        # Persist LlamaIndex metadata
        index.storage_context.persist(persist_dir=INDEX_DIR)

        # Persist FAISS explicitly
        faiss.write_index(faiss_index, str(faiss_path))

        print("arXiv index built and cached")

    return index.as_retriever(similarity_top_k=5)
