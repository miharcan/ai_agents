class AgentKernel:
    def __init__(self):
        self.state = {}
        self.memory = {}
        self.tools = ToolRegistry()

    def think(self, user_input):
        observations = self.state.get("observations", [])

        obs_text = "\n".join(observations) if observations else "None"

        return f"""
    Thought:
    User question: "{user_input}"

    Evidence gathered so far:
    {obs_text}

    I should decide:
    - What I already know
    - What I still need to know
    - Whether another tool call is required
    """

    def act(self, thought):
        return {"action": "noop"}

    def observe(self, result):
        self.state.setdefault("observations", []).append(result)

    def run(self, user_input):
        thought = self.think(user_input)
        action = self.act(thought)
        self.observe(action)
        return f"Final answer using {action}"
    
    def route_tools(self, thought):
        thought_lower = thought.lower()
        observations = " ".join(self.state.get("observations", [])).lower()

        # If question is about system behavior and we haven't looked at logs yet
        if any(k in thought_lower for k in ["boot", "issue", "anomaly", "error"]):
            if "linux" not in observations:
                return ("search_linux_logs", {"query": thought})

        # If question asks for explanation or cause and we lack theory
        if any(k in thought_lower for k in ["why", "explain", "cause", "theory"]):
            if "paper" not in observations and "research" not in observations:
                return ("search_arxiv", {"query": thought})

        return None


class ToolRegistry:
    def __init__(self):
        self._tools = {}

    def register(self, tool):
        self._tools[tool.name] = tool

    def call(self, name, **kwargs):
        if name not in self._tools:
            raise ValueError(f"Tool '{name}' not registered")
        return self._tools[name](**kwargs)

    def list_tools(self):
        return list(self._tools.keys())
