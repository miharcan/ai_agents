from core.react_agent import ReActAgent
from core.tools import RuntimeEvidenceTool, ArxivSearchTool
from rag.linux_index import load_linux_retriever
from rag.document_index import load_docs


def main(query, llm_backend, domain):
    agent = ReActAgent(llm_backend=llm_backend)
    agent.state["domain"] = domain

    if domain == "runtime":
        retriever = load_linux_retriever(
            "data/sources/linux/Linux.log"
        )
        agent.tools.register(
            RuntimeEvidenceTool(linux_retriever=retriever)
        )

    elif domain == "knowledge":
        arxiv_retriever = load_docs()
        agent.tools.register(
            ArxivSearchTool(arxiv_retriever)
        )

    answer = agent.run(query)
    print(answer)
