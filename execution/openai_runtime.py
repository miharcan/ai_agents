import os
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

USE_MOCK = False


def calculate(a: float, b: float) -> float:
    return a + b


# ✅ Correct 2025 OpenAI Responses API tool schema
tools = [
    {
        "type": "function",
        "name": "calculate",
        "description": "Add two numbers",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "number"},
                "b": {"type": "number"}
            },
            "required": ["a", "b"]
        }
    }
]


def run_with_openai(query: str):
    if USE_MOCK:
        return {"mock": True, "input": query, "tool_demo": calculate(a=2, b=3)}

    # --- Primary model call ---
    response = client.responses.create(
        model="gpt-4.1",
        input=query,
        tools=tools    # must include "type": "function"
    )

    output = response.output[0]

    # --- If tool call ---
    if output.type == "tool_call":
        fn_name = output.tool_call.name
        args = output.tool_call.arguments

        if fn_name == "calculate":
            result = calculate(**args)

            # --- Feed result back to LLM ---
            follow_up = client.responses.create(
                model="gpt-4.1",
                input=f"Tool result for {fn_name}: {result}"
            )
            return follow_up.output_text

    # --- Normal answer ---
    return response.output_text
