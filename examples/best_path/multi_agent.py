from execution.llm_runtime import run_llm
from rag.document_index import load_docs

def main(query: str, llm_backend: str):
    print(f"LLM backend: {llm_backend}")

    retriever = load_docs()
    nodes = retriever.retrieve(query)

    context = "\n\n".join(
        node.get_content() for node in nodes
    )

    synthesis_prompt = f"""
You are a senior research agent.

You have retrieved the following research context:
{context}

Your task:
- Synthesize a coherent, high-level answer
- Cite themes and insights
- Be concise and factual

Question:
{query}

Answer:
"""

    result = run_llm(synthesis_prompt, backend=llm_backend)
    print(result)
