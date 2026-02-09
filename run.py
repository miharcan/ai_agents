import argparse


def run_single(query, llm_backend, domain):
    from examples.best_path import single_agent
    single_agent.main(query, llm_backend, domain)


def run_react(query, llm_backend, domain):
    from examples.best_path import react_agent
    react_agent.main(query, llm_backend, domain)


def run_rag(query, llm_backend, domain):
    from examples.best_path import rag_agent
    rag_agent.main(query, llm_backend, domain)


def run_multi(query, llm_backend, domain):
    from examples.best_path import multi_agent
    multi_agent.main(query, llm_backend, domain)


def main():
    parser = argparse.ArgumentParser(
        description="AI Agents Playground"
    )

    parser.add_argument(
        "--mode",
        choices=["single", "react", "rag", "multi"],
        required=True,
        help="Which agent demo to run",
    )

    parser.add_argument(
        "--query",
        required=True,
        help="User query"
    )

    parser.add_argument(
        "--llm",
            choices=["openai", "tiny", "mistral", "llama3", "phi3"],
        default="openai",
        help="LLM backend"
    )

    parser.add_argument(
        "--domain",
        choices=["runtime", "knowledge"],
        default="runtime",
        help="Epistemic domain"
    )

    parser.add_argument(
        "--compare",
        nargs=2,
        choices=["normal", "abnormal"],
        help="Compare two runtime baselines"
    )

    parser.add_argument(
        "--current-logs",
        type=str,
        help="Path to current incident logs (ephemeral)"
    )

    args = parser.parse_args()

    if args.mode == "single":
        run_single(args.query, args.llm, args.domain)
    elif args.mode == "react":
        run_react(args.query, args.llm, args.domain)
    elif args.mode == "rag":
        run_rag(args.query, args.llm, args.domain)
    elif args.mode == "multi":
        run_multi(args.query, args.llm, args.domain)


if __name__ == "__main__":
    main()
