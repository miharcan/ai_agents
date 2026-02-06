from core.react_agent import ReActAgent
from core.tools import RuntimeEvidenceTool, ArxivSearchTool
from rag.linux_index import load_linux_retriever
from rag.document_index import load_docs


def main(query, llm_backend, domain):
    # Coordinator / primary agent
    coordinator = ReActAgent(llm_backend=llm_backend)
    coordinator.state["domain"] = domain

    # --- Domain-specific tool wiring ---
    if domain == "runtime":
        linux_retriever = load_linux_retriever(
            "data/sources/linux/Linux.log"
        )
        coordinator.tools.register(
            RuntimeEvidenceTool(linux_retriever=linux_retriever)
        )

    elif domain == "knowledge":
        arxiv_retriever = load_docs()
        coordinator.tools.register(
            ArxivSearchTool(arxiv_retriever)
        )

    # --- Run ---
    answer = coordinator.run(query)
    print(answer)
