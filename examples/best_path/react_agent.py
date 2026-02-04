from core.react_agent import ReActAgent

def main(query: str, llm_backend: str):
    agent = ReActAgent(llm_backend)
    result = agent.run(query)
    print(result)
