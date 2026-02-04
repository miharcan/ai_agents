from execution.llm_runtime import run_llm

def main(query: str, llm_backend: str):
    response = run_llm(query, backend=llm_backend)
    print(response)

if __name__ == "__main__":
    main()
