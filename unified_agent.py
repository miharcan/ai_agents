from core.react_agent import ReActAgent
from orchestration.langgraph_graph import app
from multiagent.autogen_agents import Researcher, Analyst, Writer
from rag.document_index import load_docs
from execution.openai_runtime import run_with_openai


def unified_agent(query):
    # ---- 1. Run RAG ----
    rag_engine = load_docs("docs/")
    rag_raw = rag_engine.query(query)

    # Extract only the answer text (no metadata, no nodes, no IDs)
    try:
        rag_answer = rag_raw.response
    except AttributeError:
        rag_answer = rag_raw  # handle mock engines
    
    # ---- 2. Multi-agent pipeline ----
    research = Researcher().run(query)
    analysis = Analyst().run(research)
    llm_result = run_with_openai(analysis)

    # ---- 3. LangGraph orchestration ----
    graph_result = app.invoke({"query": query})

    # Extract final graph answer
    graph_answer = graph_result.get("final_answer", None)

    # ---- 4. Pick best overall answer ----
    final_answer = rag_answer or graph_answer or "No answer found."

    # ---- 5. Return clean structured output ----
    return {
        "answer": final_answer,
        "components": {
            "rag": rag_answer,
            "multiagent": llm_result,
            "graph": graph_result
        }
    }
