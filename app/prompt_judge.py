import json

from app.generator import client, MODEL_NAME


# ============================================================
# Helper:
# Clean Gemini JSON responses
# ============================================================

def _clean_json_response(text):

    if not text:
        raise ValueError(
            "Gemini returned an empty response."
        )

    text = text.strip()

    if text.startswith("```json"):
        text = text[len("```json"):].strip()

    elif text.startswith("```"):
        text = text[len("```"):].strip()

    if text.endswith("```"):
        text = text[:-3].strip()

    return text


# ============================================================
# Helper:
# Parse JSON safely
# ============================================================

def _parse_json_response(text):

    cleaned_text = _clean_json_response(
        text
    )

    try:

        return json.loads(
            cleaned_text
        )

    except json.JSONDecodeError as error:

        raise ValueError(
            "Gemini returned invalid JSON.\n\n"
            f"Raw response:\n{cleaned_text}"
        ) from error


# ============================================================
# Output Quality Evaluation
# ============================================================

def judge_output_quality_batch(
    user_prompt,
    task_analysis,
    evaluation_items
):

    evaluation_focus = task_analysis.get(
        "evaluation_focus",
        []
    )

    expected_output = task_analysis.get(
        "expected_output",
        ""
    )

    task_summary = task_analysis.get(
        "task_summary",
        ""
    )

    evaluation_prompt = f"""
You are an expert evaluator for an AI prompt optimization system.

Your job is to evaluate the QUALITY OF THE GENERATED OUTPUT.

You are NOT evaluating how well the prompt is written.

You are evaluating whether the generated answer actually
performs the user's task successfully.

ORIGINAL USER PROMPT:
{user_prompt}

TASK SUMMARY:
{task_summary}

EXPECTED OUTPUT:
{expected_output}

EVALUATION FOCUS:
{evaluation_focus}


Evaluate every generated output against the SAME original task.

Use the scenario to determine whether the output appropriately
handles the specific situation.

IMPORTANT EVALUATION RULES:

1. Judge the generated output itself.

2. Do not give a perfect score simply because the output is
   generally well-written.

3. A response should receive a high score only when it
   actually satisfies the important requirements of the task.

4. Use the EXPECTED OUTPUT and EVALUATION FOCUS as important
   evidence of what a successful answer should contain.

5. If the task analysis identifies specific expected elements,
   check whether the generated output actually contains them
   when they are applicable.

6. Do not penalize an output for information that the scenario
   does not provide.

7. Do not invent requirements that are not supported by the
   original prompt, task analysis, or scenario.

8. Do not reward unnecessary verbosity.

9. A concise answer can receive a perfect score if it fully
   satisfies the task.

10. A fluent or grammatically correct answer is NOT automatically
    a high-quality answer.

11. Missing important task requirements should reduce the score.

12. Score each criterion independently.

Use scores between 0.0 and 1.0.

Scoring guidance:

1. Task Completion
   1.0 = Fully completes the requested task.
   0.75 = Mostly completes the task with a minor omission.
   0.50 = Partially completes the task.
   0.25 = Major parts of the task are missing.
   0.0 = Does not complete the task.

2. Requirement Satisfaction
   1.0 = Satisfies essentially all relevant requirements.
   0.75 = Satisfies most requirements with a minor omission.
   0.50 = Satisfies only some requirements.
   0.25 = Misses most important requirements.
   0.0 = Fails the requirements.

3. Scenario Appropriateness
   1.0 = Directly and appropriately handles the scenario.
   0.75 = Appropriate with a minor weakness.
   0.50 = Only partially adapted to the scenario.
   0.25 = Poorly handles the scenario.
   0.0 = Ignores or contradicts the scenario.

4. Expected Output Alignment
   1.0 = Closely matches the expected form and important
         content described by the task analysis.
   0.75 = Mostly aligned with a minor omission.
   0.50 = Partially aligned.
   0.25 = Poorly aligned.
   0.0 = Fundamentally different from the expected output.


EVALUATION ITEMS:

{json.dumps(
    evaluation_items,
    indent=2
)}


Return ONLY valid JSON in exactly this format:

{{
    "evaluations": [
        {{
            "prompt_name": "",
            "scenario_id": 1,
            "scores": {{
                "task_completion": 0.0,
                "requirement_satisfaction": 0.0,
                "scenario_appropriateness": 0.0,
                "expected_output_alignment": 0.0
            }},
            "reasoning": ""
        }}
    ]
}}

Return exactly one evaluation for every evaluation item.

Do not omit any item.
Do not add extra evaluations.
"""


    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=evaluation_prompt
    )


    parsed = _parse_json_response(
        response.text
    )


    if "evaluations" not in parsed:

        raise ValueError(
            "Output quality judge response is missing "
            "'evaluations'."
        )


    expected_count = len(
        evaluation_items
    )

    actual_count = len(
        parsed["evaluations"]
    )


    if actual_count != expected_count:

        raise ValueError(
            "Output quality judge returned "
            f"{actual_count} evaluations, expected "
            f"{expected_count}."
        )


    evaluations = []


    for evaluation in parsed[
        "evaluations"
    ]:

        scores = evaluation.get(
            "scores"
        )

        if not scores:

            raise ValueError(
                "Output quality evaluation is missing "
                "'scores'."
            )


        required_scores = [
            "task_completion",
            "requirement_satisfaction",
            "scenario_appropriateness",
            "expected_output_alignment"
        ]


        for criterion in required_scores:

            if criterion not in scores:

                raise ValueError(
                    f"Missing output quality criterion: "
                    f"{criterion}"
                )


            score = scores[
                criterion
            ]


            if not isinstance(
                score,
                (int, float)
            ):

                raise ValueError(
                    f"Score for {criterion} must be numeric."
                )


            if score < 0.0 or score > 1.0:

                raise ValueError(
                    f"Score for {criterion} must be "
                    "between 0.0 and 1.0."
                )


        output_quality_score = (

            scores[
                "task_completion"
            ]

            + scores[
                "requirement_satisfaction"
            ]

            + scores[
                "scenario_appropriateness"
            ]

            + scores[
                "expected_output_alignment"
            ]

        ) / 4


        evaluations.append(
            {
                "prompt_name": (
                    evaluation[
                        "prompt_name"
                    ]
                ),

                "scenario_id": (
                    evaluation[
                        "scenario_id"
                    ]
                ),

                "output_quality_score": (
                    output_quality_score
                ),

                "output_scores": scores,

                "reasoning": (
                    evaluation.get(
                        "reasoning",
                        ""
                    )
                )
            }
        )


    return {
        "evaluations": evaluations
    }


# ============================================================
# Prompt Effectiveness Evaluation
# ============================================================

def judge_prompt_effectiveness_batch(
    user_prompt,
    task_analysis,
    evaluation_items,
    optimization_requirements=None
):

    task_summary = task_analysis.get(
        "task_summary",
        ""
    )

    expected_output = task_analysis.get(
        "expected_output",
        ""
    )

    evaluation_focus = task_analysis.get(
        "evaluation_focus",
        []
    )


    # --------------------------------------------------------
    # Extract unique prompts
    # --------------------------------------------------------

    unique_prompts = {}

    for item in evaluation_items:

        prompt_name = item[
            "prompt_name"
        ]

        prompt = item[
            "prompt"
        ]

        unique_prompts[
            prompt_name
        ] = prompt


    prompts_for_judge = []


    for prompt_name, prompt in (
        unique_prompts.items()
    ):

        prompts_for_judge.append(
            {
                "prompt_name": prompt_name,
                "prompt": prompt
            }
        )


    optimization_section = ""

    if optimization_requirements:

        optimization_section = f"""
USER'S ADDITIONAL OPTIMIZATION REQUIREMENTS:

{optimization_requirements}

These requirements describe what the user specifically wants
the optimized prompts to improve.

Evaluate whether each candidate addresses them appropriately.
Do not reward unnecessary verbosity.
"""


    prompt = f"""
You are an expert evaluator for an AI prompt optimization system.

Your job is to evaluate HOW EFFECTIVE EACH PROMPT IS at
instructing an AI model to perform the original task.

You are evaluating the PROMPT ITSELF.

Do not evaluate the generated answer here.

ORIGINAL USER PROMPT:
{user_prompt}

TASK SUMMARY:
{task_summary}

EXPECTED OUTPUT:
{expected_output}

EVALUATION FOCUS:
{evaluation_focus}

{optimization_section}


PROMPTS TO EVALUATE:

{json.dumps(
    prompts_for_judge,
    indent=2
)}


Evaluate each prompt using exactly these five criteria:

1. Task Clarity
   Does the prompt clearly communicate what the AI must do?

2. Requirement Coverage
   Does the prompt explicitly cover important requirements
   supported by the original task?

3. Output Specification
   Does the prompt provide useful guidance about the expected
   output when such guidance is beneficial?

4. Constraint Handling
   Does the prompt specify important constraints, boundaries,
   tone, format, length, exclusions, or other requirements
   when appropriate?

5. Ambiguity Reduction
   Does the prompt reduce ambiguity that could cause inconsistent
   or incorrect outputs?


IMPORTANT RULES:

1. Compare each candidate against the ORIGINAL USER PROMPT,
   not against verbosity.

2. A longer prompt is NOT automatically better.

3. A concise prompt can receive a high score if it provides
   the necessary instruction efficiently.

4. Do not reward instructions that are irrelevant to the task.

5. Do not penalize a prompt for failing to include information
   that is impossible to know from the original task.

6. Do not invent requirements.

7. If an optimization requirement says to keep the prompt
   concise, evaluate whether useful instructions were added
   efficiently rather than rewarding length.

8. A prompt should improve the model's ability to consistently
   produce the desired output.

9. The baseline should be judged according to how much useful
   task guidance it provides, not simply whether the underlying
   task is understandable.

10. Candidate prompts should receive higher scores only when
    they genuinely improve instruction quality.


Use scores between 0.0 and 1.0.

Return ONLY valid JSON in exactly this format:

{{
    "evaluations": [
        {{
            "prompt_name": "",
            "scores": {{
                "task_clarity": 0.0,
                "requirement_coverage": 0.0,
                "output_specification": 0.0,
                "constraint_handling": 0.0,
                "ambiguity_reduction": 0.0
            }}
        }}
    ]
}}

Return exactly one evaluation for every unique prompt.

Do not add extra criteria.
Do not omit any prompt.
"""


    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )


    parsed = _parse_json_response(
        response.text
    )


    if "evaluations" not in parsed:

        raise ValueError(
            "Prompt effectiveness judge response "
            "is missing 'evaluations'."
        )


    expected_count = len(
        unique_prompts
    )

    actual_count = len(
        parsed["evaluations"]
    )


    if actual_count != expected_count:

        raise ValueError(
            "Prompt effectiveness judge returned "
            f"{actual_count} evaluations, expected "
            f"{expected_count}."
        )


    required_scores = [
        "task_clarity",
        "requirement_coverage",
        "output_specification",
        "constraint_handling",
        "ambiguity_reduction"
    ]


    evaluations = []


    for evaluation in parsed[
        "evaluations"
    ]:

        scores = evaluation.get(
            "scores"
        )


        if not scores:

            raise ValueError(
                "Prompt effectiveness evaluation "
                "is missing 'scores'."
            )


        for criterion in required_scores:

            if criterion not in scores:

                raise ValueError(
                    "Missing prompt effectiveness "
                    f"criterion: {criterion}"
                )


            score = scores[
                criterion
            ]


            if not isinstance(
                score,
                (int, float)
            ):

                raise ValueError(
                    f"Score for {criterion} must be numeric."
                )


            if score < 0.0 or score > 1.0:

                raise ValueError(
                    f"Score for {criterion} must be "
                    "between 0.0 and 1.0."
                )


        prompt_effectiveness_score = (

            scores[
                "task_clarity"
            ]

            + scores[
                "requirement_coverage"
            ]

            + scores[
                "output_specification"
            ]

            + scores[
                "constraint_handling"
            ]

            + scores[
                "ambiguity_reduction"
            ]

        ) / 5


        evaluations.append(
            {
                "prompt_name": (
                    evaluation[
                        "prompt_name"
                    ]
                ),

                "prompt_effectiveness_score": (
                    prompt_effectiveness_score
                ),

                "prompt_effectiveness_scores": (
                    scores
                )
            }
        )


    return {
        "evaluations": evaluations
    }


# ============================================================
# Combined Judge
# ============================================================

def judge_outputs_batch(
    user_prompt,
    task_analysis,
    evaluation_items,
    optimization_requirements=None
):

    # --------------------------------------------------------
    # Evaluate generated outputs
    # --------------------------------------------------------

    output_quality_response = (
        judge_output_quality_batch(
            user_prompt,
            task_analysis,
            evaluation_items
        )
    )


    output_evaluations = (
        output_quality_response[
            "evaluations"
        ]
    )


    # --------------------------------------------------------
    # Evaluate prompts
    # --------------------------------------------------------

    prompt_effectiveness_response = (
        judge_prompt_effectiveness_batch(
            user_prompt,
            task_analysis,
            evaluation_items,
            optimization_requirements
        )
    )


    prompt_evaluations = (
        prompt_effectiveness_response[
            "evaluations"
        ]
    )


    # --------------------------------------------------------
    # Convert prompt effectiveness evaluations
    # into a lookup dictionary
    # --------------------------------------------------------

    prompt_effectiveness_lookup = {}


    for evaluation in prompt_evaluations:

        prompt_name = evaluation[
            "prompt_name"
        ]

        prompt_effectiveness_lookup[
            prompt_name
        ] = evaluation


    # --------------------------------------------------------
    # Combine both evaluation types
    # --------------------------------------------------------

    combined_evaluations = []


    for output_evaluation in output_evaluations:

        prompt_name = output_evaluation[
            "prompt_name"
        ]


        if prompt_name not in (
            prompt_effectiveness_lookup
        ):

            raise ValueError(
                "No prompt effectiveness evaluation "
                f"found for {prompt_name}."
            )


        prompt_evaluation = (
            prompt_effectiveness_lookup[
                prompt_name
            ]
        )


        output_quality_score = (
            output_evaluation[
                "output_quality_score"
            ]
        )


        prompt_effectiveness_score = (
            prompt_evaluation[
                "prompt_effectiveness_score"
            ]
        )


        # ----------------------------------------------------
        # Existing scoring formula
        #
        # 70% output quality
        # 30% prompt effectiveness
        # ----------------------------------------------------

        overall_score = (

            0.70
            * output_quality_score

            +

            0.30
            * prompt_effectiveness_score

        )


        combined_evaluations.append(
            {
                "prompt_name": prompt_name,

                "scenario_id": (
                    output_evaluation[
                        "scenario_id"
                    ]
                ),

                "output_quality_score": (
                    output_quality_score
                ),

                "prompt_effectiveness_score": (
                    prompt_effectiveness_score
                ),

                "overall_score": (
                    overall_score
                ),

                "output_scores": (
                    output_evaluation[
                        "output_scores"
                    ]
                ),

                "prompt_effectiveness_scores": (
                    prompt_evaluation[
                        "prompt_effectiveness_scores"
                    ]
                ),

                "reasoning": (
                    output_evaluation[
                        "reasoning"
                    ]
                )
            }
        )


    return {
        "evaluations": combined_evaluations
    }