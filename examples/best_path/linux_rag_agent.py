from rag.document_index import DocumentIndex
from rag.linux_log_loader import load_linux_documents
from execution.local_runtime import LocalRuntime


def main():
    # --- Runtime (reuse what you already have) ---
    runtime = LocalRuntime()

    # --- Index ---
    index = DocumentIndex(
        index_name="linux_logs",
        persist_path="data/linux_index",  # keep as-is per your decision
        runtime=runtime,
    )

    # --- Load Linux documents ---
    docs = load_linux_documents("data/sources/linux/Linux.log")

    # --- Index them ---
    index.add_documents(docs)

    # --- Query ---
    query = "What happened during system startup?"

    results = index.query(query, top_k=3)

    print("\n=== Query ===")
    print(query)

    print("\n=== Retrieved Context ===")
    for r in results:
        print("-", r["text"])

    print("\n=== Answer ===")
    answer = runtime.complete(
        prompt=f"""
You are a Linux systems expert.

Using the following context, answer the question clearly and concisely.

Context:
{results[0]["text"]}

Question:
{query}
"""
    )

    print(answer)


if __name__ == "__main__":
    main()
