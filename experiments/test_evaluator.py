from app.evaluator import (
    evaluate_prompts
)


user_prompt = """
Write an email to a client about
a project delay.
"""


optimization_requirements = """
Make the prompt more effective while
keeping it concise.
"""


results = evaluate_prompts(
    user_prompt,
    optimization_requirements
)


print(
    "\n"
    + "=" * 70
)

print(
    "GENERATED PROMPTS"
)

print(
    "=" * 70
)


for result in results[
    "results"
]:

    print(
        f"\n{result['prompt_name']}"
    )

    print(
        "-" * 40
    )

    print(
        result["prompt"]
    )


print(
    "\n"
    + "=" * 70
)

print(
    "PROMPT EVALUATION RESULTS"
)

print(
    "=" * 70
)


for result in results[
    "results"
]:

    print(
        f"\n{result['prompt_name']}"
    )

    print(
        "-" * 40
    )


    print(
        "Average Output Quality: "
        f"{result['average_output_quality_score']:.3f}"
    )


    print(
        "Average Prompt Effectiveness: "
        f"{result['average_prompt_effectiveness_score']:.3f}"
    )


    print(
        "Average Overall Score: "
        f"{result['average_overall_score']:.3f}"
    )


    print(
        "Minimum Output Quality: "
        f"{result['minimum_output_quality_score']:.3f}"
    )


    print(
        "Average Input Tokens "
        "Per Scenario: "
        f"{result['average_input_tokens']:.1f}"
    )


    print(
        "Average Output Tokens "
        "Per Scenario: "
        f"{result['average_output_tokens']:.1f}"
    )


    print(
        "Average Total Tokens "
        "Per Scenario: "
        f"{result['average_total_tokens']:.1f}"
    )


print(
    "\n"
    + "=" * 70
)

print(
    "BEST PROMPT"
)

print(
    "=" * 70
)


print(
    results[
        "best_prompt"
    ][
        "prompt_name"
    ]
)


print(
    "\nPrompt:\n"
)


print(
    results[
        "best_prompt"
    ][
        "prompt"
    ]
)


print(
    "\nOutput Quality: "
    f"{results['best_prompt']['average_output_quality_score']:.3f}"
)


print(
    "Prompt Effectiveness: "
    f"{results['best_prompt']['average_prompt_effectiveness_score']:.3f}"
)


print(
    "Overall Score: "
    f"{results['best_prompt']['average_overall_score']:.3f}"
)


print(
    "Minimum Output Quality: "
    f"{results['best_prompt']['minimum_output_quality_score']:.3f}"
)


print(
    "\nSelection Reason:"
)


print(
    results[
        "best_prompt"
    ][
        "selection_reason"
    ]
)