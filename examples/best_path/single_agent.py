from execution.openai_runtime import run_with_openai

def main(query):

    response = run_with_openai(query)

    print("\n=== SINGLE AGENT OUTPUT ===\n")
    print(response)

if __name__ == "__main__":
    main()
