from core.agent_kernel import AgentKernel

class ReActAgent(AgentKernel):
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
        return self.final_answer(steps)
