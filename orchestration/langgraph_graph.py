from typing import TypedDict
from langgraph.graph import StateGraph
from execution.openai_runtime import run_with_openai


# ---- Define the state schema (required by LangGraph >=0.2.x) ----
class AgentState(TypedDict, total=False):
    query: str
    plan: str
    result: str
    final_answer: str
    next: str


# ---- Node functions ----
def planner(state: AgentState):
    q = state.get("query", "")
    return {
        "plan": f"search about {q}",
    }


def worker(state):
    plan = state.get("plan", "")
    result = run_with_openai(plan)
    return {"result": result}



def finalizer(state: AgentState):
    return {
        "final_answer": state.get("result")
    }


# ---- Build LangGraph ----
graph = StateGraph(AgentState)

graph.add_node("plan", planner)
graph.add_node("work", worker)
graph.add_node("final", finalizer)

graph.set_entry_point("plan")

graph.add_edge("plan", "work")
graph.add_edge("work", "final")

# ---- Compile the graph into an executable agent ----
app = graph.compile()
