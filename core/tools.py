class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, name, fn):
        self.tools[name] = fn
    
    def call(self, name, **kwargs):
        return self.tools[name](**kwargs)
