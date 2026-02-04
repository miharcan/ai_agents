from core.react_agent import ReActAgent

def main(query):
    agent = ReActAgent()
    
    response = agent.run(query)

    print("\n=== REACT AGENT OUTPUT ===\n")
    print(response)

if __name__ == "__main__":
    main()
