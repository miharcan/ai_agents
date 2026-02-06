from core.react_agent import ReActAgent
from core.tools import RuntimeEvidenceTool, ArxivSearchTool  # runtime evidence
from rag.linux_index import load_linux_retriever
from rag.document_index import load_docs   # arXiv retriever
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--domain",
        choices=["runtime", "knowledge"],
        default="runtime",
    )
    args = parser.parse_args()

    agent = ReActAgent(llm_backend="local")
    agent.state["domain"] = args.domain

    # --- Tool wiring depends on domain ---
    if args.domain == "runtime":
        retriever = load_linux_retriever(
            "data/sources/linux/Linux.log"
        )
        agent.tools.register(
            RuntimeEvidenceTool(linux_retriever=retriever)
        )

    elif args.domain == "knowledge":
        arxiv_retriever = load_docs()
        agent.tools.register(
            ArxivSearchTool(arxiv_retriever)
        )

    question = "Are there any issues or anomalies in this Linux boot?"
    answer = agent.run(question)

    print("\n=== Domain ===")
    print(args.domain)

    print("\n=== Question ===")
    print(question)

    print("\n=== ReAct Answer ===")
    print(answer)


if __name__ == "__main__":
    main()
