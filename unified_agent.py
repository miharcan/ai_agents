from rag.document_index import load_docs
from execution.openai_runtime import run_with_openai
from multiagent.autogen_agents import Researcher, Analyst
from orchestration.langgraph_graph import app


def unified_agent(query):
    # ---- 1. RAG (retrieval only) ----
    retriever = load_docs("docs/")
    nodes = retriever.retrieve(query)
    context = "\n".join(node.text for node in nodes)

    rag_prompt = f"""
You are a strategy assistant.

Use the following internal documents as source of truth:

{context}

Question:
{query}

Provide a concise, accurate answer grounded in the documents.
"""

    rag_answer = run_with_openai(rag_prompt)

    # ---- 2. Multi-agent reasoning ----
    research = Researcher().run(query)
    analysis = Analyst().run(research)
    multiagent_answer = run_with_openai(analysis)

    # ---- 3. LangGraph orchestration ----
    graph_result = app.invoke({"query": query})
    graph_answer = graph_result.get("final_answer")

    # ---- 4. Select best answer (simple heuristic for demo) ----
    final_answer = rag_answer or graph_answer or multiagent_answer

    # ---- 5. Return structured output ----
    return {
        "answer": final_answer,
        "components": {
            "rag": rag_answer,
            "multiagent": multiagent_answer,
            "graph": graph_result,
        },
    }
