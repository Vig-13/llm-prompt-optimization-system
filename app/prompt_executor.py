import json

from app.generator import client, MODEL_NAME


def execute_prompt_batch(
    prompt,
    scenarios
):

    formatted_scenarios = ""

    for scenario in scenarios:

        formatted_scenarios += f"""

SCENARIO {scenario["id"]}:

{scenario["description"]}

"""

    execution_prompt = f"""
You are an AI assistant completing a task.

Follow the instruction below.

INSTRUCTION:
{prompt}

You must complete the instruction separately
for each scenario provided below.

{formatted_scenarios}

Return ONLY valid JSON in this format:

{{
    "results": [
        {{
            "scenario_id": 1,
            "output": ""
        }},
        {{
            "scenario_id": 2,
            "output": ""
        }}
    ]
}}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=execution_prompt
    )

    result = response.text.strip()

    if not result:
        raise ValueError(
            "Gemini returned an empty response."
        )

    if result.startswith("```json"):
        result = result.replace(
            "```json",
            "",
            1
        )

    if result.startswith("```"):
        result = result.replace(
            "```",
            "",
            1
        )

    if result.endswith("```"):
        result = result.rsplit(
            "```",
            1
        )[0]

    result = result.strip()

    parsed_result = json.loads(result)

    usage = response.usage_metadata

    return {
        "results": parsed_result["results"],
        "token_usage": {
            "input_tokens": (
                usage.prompt_token_count
            ),
            "output_tokens": (
                usage.candidates_token_count
            ),
            "total_tokens": (
                usage.total_token_count
            )
        }
    }