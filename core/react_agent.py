from core.agent_kernel import AgentKernel
from execution.llm_runtime import run_llm

class ReActAgent(AgentKernel):
    def __init__(self, llm_backend: str):
        self.llm_backend = llm_backend
        super().__init__()

    def run(self, query):
        steps = []

        for _ in range(3):
            thought = self.think(query)
            tool_call = self.route_tools(thought)

            if tool_call:
                name, args = tool_call
                result = self.tools.call(name, **args)
                steps.append((thought, name, args, result))
                self.observe(result)

        return self.final_answer(query, steps)

    def final_answer(self, query, steps):
        """
        Synthesize a final answer from ReAct reasoning steps.
        """
        reasoning = "\n".join(str(step) for step in steps)

        prompt = f"""
You are a reasoning agent.

Original question:
{query}

Reasoning trace:
{reasoning}

Provide a clear, concise final answer to the original question.
"""

        return run_llm(prompt, backend=self.llm_backend)
