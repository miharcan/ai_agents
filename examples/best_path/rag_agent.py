from core.react_agent import ReActAgent
from core.tools import RuntimeEvidenceTool, ArxivSearchTool
from rag.linux_index import load_linux_retriever
from rag.openstack_index import load_openstack_retriever
from rag.document_index import load_docs


def main(query, llm_backend, domain):
    agent = ReActAgent(llm_backend=llm_backend)
    agent.state["domain"] = domain
    

    # --- Domain-specific RAG ---
    if domain == "runtime":
        linux = load_linux_retriever("data/sources/linux/Linux.log")
        openstack = load_openstack_retriever("data/sources/openstack/abnormal/")

        agent.tools.register(
            RuntimeEvidenceTool(
                linux_retriever=linux,
                openstack_retriever=openstack
            )
        )

    elif domain == "knowledge":
        arxiv_retriever = load_docs()
        agent.tools.register(
            ArxivSearchTool(arxiv_retriever)
        )

    answer = agent.run(query)
    print(answer)
