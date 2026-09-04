import json

from app.generator import client, MODEL_NAME


def analyze_task(user_prompt):

    prompt = f"""
Analyze the following user prompt.

Your job is to identify the task the user wants to perform.

Return ONLY valid JSON in the following format:

{{
    "task_type": "",
    "task_summary": "",
    "expected_output": "",
    "evaluation_focus": []
}}

Definitions:

task_type:
A short category describing the task.

Examples include:
- text generation
- email writing
- summarization
- classification
- information extraction
- question answering
- code generation
- translation
- data analysis

task_summary:
Briefly explain what the user is asking
the model to do.

expected_output:
Describe what the expected output should
generally look like.

evaluation_focus:
List the important aspects that should be
checked when evaluating the quality
of the output.

User Prompt:

{user_prompt}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    result = response.text.strip()

    print("\nRAW TASK ANALYSIS RESPONSE:")
    print(repr(result))

    if not result:

        raise ValueError(
            "Gemini returned an empty "
            "task analysis response."
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