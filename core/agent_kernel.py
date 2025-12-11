class AgentKernel:
    def __init__(self):
        self.state = {}
        self.memory = {}

    def think(self, user_input):
        return f"Thought: I should process {user_input}"

    def act(self, thought):
        return {"action": "noop"}

    def observe(self, result):
        self.state["last_observation"] = result

    def run(self, user_input):
        thought = self.think(user_input)
        action = self.act(thought)
        self.observe(action)
        return f"Final answer using {action}"
    
    def route_tools(self, thought):
        # simple rule-based router
        if "add" in thought:
            return ("add", {"a": 5, "b": 7})
        return None


