from rag.document_index import load_docs
from execution.openai_runtime import run_with_openai


def main(query):
    retriever = load_docs()

    nodes = retriever.retrieve(query)

    context = "\n\n".join(
        f"Title: {n.metadata.get('title', '')}\n{n.text}"
        for n in nodes
    )

    prompt = f"""
You are a research assistant.

Using the following retrieved arXiv abstracts, answer the question below.
Focus on summarising themes, methods, and key findings.
Do not invent citations beyond what is provided.

Retrieved papers:
{context}

Question:
{query}

Answer:
"""

    answer = run_with_openai(prompt)

    print("\n=== RAG AGENT OUTPUT (arXiv-grounded) ===\n")
    print(answer)
