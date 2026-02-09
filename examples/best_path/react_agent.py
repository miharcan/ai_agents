from core.react_agent import ReActAgent
from core.tools import RuntimeEvidenceTool, ArxivSearchTool, OpenStackCompareTool
from rag.linux_index import load_linux_retriever
from rag.document_index import load_docs
from rag.openstack_compare import load_openstack_comparison_retriever


def make_agent(llm_backend, domain):
    agent = ReActAgent(llm_backend=llm_backend)
    agent.state["domain"] = domain

    if domain == "runtime":
        linux = load_linux_retriever("data/sources/linux/Linux.log")
        openstack = load_openstack_comparison_retriever(
            normal_path="data/sources/openstack/normal",
            abnormal_path="data/sources/openstack/abnormal",
        )

        runtime_tool = RuntimeEvidenceTool(
            linux_retriever=linux,
            openstack_retriever=openstack,
        )

        agent.tools.register(runtime_tool)
        agent.tools.register(OpenStackCompareTool(runtime_tool))

        # agent.tools.register(
        #     "search_runtime_evidence",
        #     runtime_tool
        # )

        # agent.tools.register(
        #     "compare_openstack",
        #     runtime_tool.compare_openstack
        # )

    elif domain == "knowledge":
        arxiv_retriever = load_docs()
        agent.tools.register(
            ArxivSearchTool(arxiv_retriever)
        )

    return agent


def run(agent, query):
    domain = agent.state.get("domain")
    compare = agent.state.get("compare")
    current_logs = agent.state.get("current_logs")

    if domain == "runtime" and compare:
        _run_runtime_comparison(agent, query, compare, current_logs)
    else:
        answer = agent.run(query)
        print(answer)

def _run_runtime_comparison(agent, query, compare, current_logs):
    """
    Runtime diagnostic mode:
    - Compare known normal vs abnormal behavior
    - Layer in current incident logs
    - Reason in deltas
    """

    # Force the agent to retrieve comparative evidence
    comparison_prompt = f"""
You are diagnosing infrastructure instability.

You MUST call the tool `compare_openstack`
before answering.

Do not answer until you have compared
normal vs abnormal OpenStack evidence.


Available tools include runtime evidence retrieval.

Task:
1. Identify signals present in abnormal but not normal
2. Check which of those appear in the current incident
3. Identify any new signals unique to the current incident
4. Explicitly state missing evidence
5. Grade confidence (high / medium / low)

User question:
{query}
"""

    # Inject incident logs as ephemeral context (NOT indexed)
    if current_logs:
        comparison_prompt += f"""

Current incident observations (human-reported, may be incomplete):

- Network bridge misconfigured
- Layer 2 networking not initialized
- Security groups not applied to instance image

Raw notes:
{current_logs}
"""

    # Run the agent with structured intent
    answer = agent.run(comparison_prompt)
    print(answer)


# Backwards compatibility (important)
def main(query, llm_backend, domain):
    agent = make_agent(llm_backend, domain)
    run(agent, query)
