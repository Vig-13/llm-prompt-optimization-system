# Generate different effective prompts
# to compare with the original prompt

import json

from app.generator import client, MODEL_NAME


def generate_candidates(
    user_prompt,
    desired_outcome=None
):

    requirements_section = ""

    if desired_outcome:

        requirements_section = f"""
ADDITIONAL USER REQUIREMENTS:

{desired_outcome}
"""

    meta_prompt = f"""
You are an expert prompt optimization system.

Your task is to generate three genuinely improved versions
of a user's original prompt.

First, understand the original intent of the user.

Preserve the fundamental goal of the original prompt.

Each candidate must be a COMPLETE, USABLE PROMPT that can be
sent directly to another AI model.

Do NOT return labels such as:
"candidate_1"
"candidate_2"
"candidate_3"

Do NOT return explanations outside the prompts.

Generate three meaningfully different optimization candidates.

The candidates should use different optimization approaches:

1. Clarity-focused:
Improve clarity and remove ambiguity while preserving
the original intent.

2. Structure-focused:
Improve organization, instruction structure, and specify
what the output should contain.

3. Constraint-focused:
Improve explicit constraints, requirements, and
instruction-following.

Each candidate should optimize for:

- Clarity
- Effectiveness
- Instruction specificity
- Appropriate output structure
- Token efficiency

Do not unnecessarily make the prompt longer.

Do not add requirements that are unrelated to the user's
original request.

Do not change the fundamental task.

IMPORTANT:
The value of each JSON field must contain the FULL optimized
prompt itself, not the field name.

For example, this is WRONG:

{{
    "candidate_1": "candidate_1"
}}

This is also WRONG:

{{
    "candidate_1": "A clearer prompt"
}}

where "A clearer prompt" is only an explanation.

The value must be a complete prompt that another AI can
execute directly.

{requirements_section}

USER'S ORIGINAL PROMPT:

{user_prompt}

Return ONLY valid JSON in exactly this format:

{{
    "candidate_1": "FULL optimized prompt here",
    "candidate_2": "FULL optimized prompt here",
    "candidate_3": "FULL optimized prompt here"
}}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=meta_prompt
    )

    text = response.text.strip()

    if not text:
        raise ValueError(
            "Gemini returned an empty candidate response."
        )

    # --------------------------------------------------------
    # Remove markdown JSON fences if Gemini adds them
    # --------------------------------------------------------

    if text.startswith("```json"):
        text = text[len("```json"):].strip()

    elif text.startswith("```"):
        text = text[len("```"):].strip()

    if text.endswith("```"):
        text = text[:-3].strip()

    # --------------------------------------------------------
    # Parse JSON
    # --------------------------------------------------------

    try:

        candidates = json.loads(text)

    except json.JSONDecodeError as error:

        raise ValueError(
            "Gemini returned invalid JSON for candidate "
            f"generation.\n\nRaw response:\n{text}"
        ) from error

    # --------------------------------------------------------
    # Validate candidate structure
    # --------------------------------------------------------

    required_candidates = [
        "candidate_1",
        "candidate_2",
        "candidate_3"
    ]

    for candidate_name in required_candidates:

        if candidate_name not in candidates:

            raise ValueError(
                f"Missing {candidate_name} "
                "from candidate generator response."
            )

        if not isinstance(
            candidates[candidate_name],
            str
        ):

            raise ValueError(
                f"{candidate_name} must contain "
                "a string prompt."
            )

        if not candidates[candidate_name].strip():

            raise ValueError(
                f"{candidate_name} contains "
                "an empty prompt."
            )

    # --------------------------------------------------------
    # Debug output
    # --------------------------------------------------------

    print(
        "\nRAW CANDIDATE GENERATOR RESPONSE:"
    )

    print(
        repr(text)
    )

    print(
        "\nPARSED CANDIDATES:"
    )

    print(
        candidates
    )

    # --------------------------------------------------------
    # Return dictionary containing the three
    # complete optimized prompts
    # --------------------------------------------------------

    return candidates