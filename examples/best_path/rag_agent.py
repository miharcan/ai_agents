from execution.llm_runtime import run_llm
from rag.document_index import load_docs

def main(query: str, llm_backend: str):
    print(f"LLM backend: {llm_backend}")

    retriever = load_docs()
    nodes = retriever.retrieve(query)

    context = "\n\n".join(
        node.get_content() for node in nodes
    )

    prompt = f"""
You are a research assistant.
Answer the question using ONLY the context below.

Context:
{context}

Question:
{query}

Answer:
"""

    response = run_llm(prompt, backend=llm_backend)
    print(response)
