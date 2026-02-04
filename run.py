import argparse
import sys


def run_single(query):
    from examples.best_path import single_agent
    single_agent.main(query)


def run_react(query):
    from examples.best_path import react_agent
    react_agent.main(query)


def run_rag(query):
    from examples.best_path import rag_agent
    rag_agent.main(query)


def run_multi(query):
    from examples.best_path import multi_agent
    multi_agent.main(query)


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

    args = parser.parse_args()

    if args.mode == "single":
        run_single(args.query)
    elif args.mode == "react":
        run_react(args.query)
    elif args.mode == "rag":
        run_rag(args.query)
    elif args.mode == "multi":
        run_multi(args.query)


if __name__ == "__main__":
    main()
