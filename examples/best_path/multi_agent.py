from unified_agent import unified_agent

def main(query):
    result = unified_agent(query)

    print("\n=== MULTI-AGENT / UNIFIED OUTPUT ===\n")
    print(result["answer"])

if __name__ == "__main__":
    main()
