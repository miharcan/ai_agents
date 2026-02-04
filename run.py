import argparse
import sys


def run_single(query, llm_backend):
    from examples.best_path import single_agent
    single_agent.main(query, llm_backend)


def run_react(query, llm_backend):
    from examples.best_path import react_agent
    react_agent.main(query, llm_backend)


def run_rag(query, llm_backend):
    from examples.best_path import rag_agent
    rag_agent.main(query, llm_backend)


def run_multi(query, llm_backend):
    from examples.best_path import multi_agent
    multi_agent.main(query, llm_backend)


def main():
    parser = argparse.ArgumentParser(
        description="AI Agents Playground – Golden Path Runner"
    )

    parser.add_argument(
        "--mode",
        type=str,
        choices=["single", "react", "rag", "multi"],
        required=True,
        help="Which agent demo to run",
    )

    parser.add_argument(
        "--query",
        type=str,
        required=True,
        help="User query to run through the agent system",
    )

    parser.add_argument(
        "--llm",
        choices=["openai", "local"],
        default="openai",
        help="LLM backend to use"
    )

    args = parser.parse_args()

    if args.mode == "single":
        run_single(args.query, args.llm)
    elif args.mode == "react":
        run_react(args.query, args.llm)
    elif args.mode == "rag":
        run_rag(args.query, args.llm)
    elif args.mode == "multi":
        run_multi(args.query, args.llm)


if __name__ == "__main__":
    main()
