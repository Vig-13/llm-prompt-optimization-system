import json

from app.generator import client, MODEL_NAME

def generate_scenarios(user_prompt, task_analysis):

    prompt = f"""
You are creating evaluation scenarios for an AI prompt optimization system.

Your goal is to generate realistic and meaningful test scenarios
for the user's original task.

USER PROMPT:
{user_prompt}

TASK ANALYSIS:

Task Type:
{task_analysis["task_type"]}

Task Summary:
{task_analysis["task_summary"]}

Expected Output:
{task_analysis["expected_output"]}

Evaluation Focus:
{task_analysis["evaluation_focus"]}


Generate exactly 2 evaluation scenarios.

The scenarios should:

1. Be relevant to the user's original task.
2. Represent meaningfully different situations, inputs, or conditions.
3. Help test whether a prompt performs consistently across
   different cases.
4. Not be based on any optimized prompt candidate.
5. Contain the information needed for the AI to perform the task.

Return ONLY valid JSON in this format:

{{
    "scenarios": [
        {{
            "id": 1,
            "description": ""
        }},
        {{
            "id": 2,
            "description": ""
        }}
    ]
}}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
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

    return json.loads(result)