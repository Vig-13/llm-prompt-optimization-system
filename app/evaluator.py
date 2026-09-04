from app.candidate_generator import (
    generate_candidates
)

from app.task_analyzer import (
    analyze_task
)

from app.scenario_generator import (
    generate_scenarios
)

from app.prompt_executor import (
    execute_prompt_batch
)

from app.prompt_judge import (
    judge_outputs_batch
)


def evaluate_prompts(
    user_prompt,
    optimization_requirements=None
):

    print(
        "\nAnalyzing task..."
    )

    # ========================================================
    # Step 1:
    # Analyze the original task
    # ========================================================

    task_analysis = analyze_task(
        user_prompt
    )


    print(
        "Generating prompt candidates..."
    )

    # ========================================================
    # Step 2:
    # Generate optimized prompt candidates
    # ========================================================

    candidates = generate_candidates(
        user_prompt,
        optimization_requirements
    )


    # ========================================================
    # Validate candidate generator output
    # ========================================================

    required_candidates = [
        "candidate_1",
        "candidate_2",
        "candidate_3"
    ]

    for candidate_name in required_candidates:

        if candidate_name not in candidates:

            raise ValueError(
                f"Candidate generator did not return "
                f"{candidate_name}."
            )

        if not isinstance(
            candidates[candidate_name],
            str
        ):

            raise ValueError(
                f"{candidate_name} is not a string."
            )

        if not candidates[
            candidate_name
        ].strip():

            raise ValueError(
                f"{candidate_name} is empty."
            )


    print(
        "Generating evaluation scenarios..."
    )

    # ========================================================
    # Step 3:
    # Generate evaluation scenarios
    # ========================================================

    scenario_data = generate_scenarios(
        user_prompt,
        task_analysis
    )

    scenarios = scenario_data[
        "scenarios"
    ]


    if not scenarios:

        raise ValueError(
            "No evaluation scenarios were generated."
        )


    # ========================================================
    # Step 4:
    # Add baseline prompt
    # ========================================================

    prompts_to_test = [

        {
            "name": "Baseline",
            "prompt": user_prompt
        }

    ]


    # ========================================================
    # Step 5:
    # IMPORTANT:
    # Extract VALUES from candidate dictionary.
    #
    # candidates is:
    #
    # {
    #     "candidate_1": "actual prompt",
    #     "candidate_2": "actual prompt",
    #     "candidate_3": "actual prompt"
    # }
    #
    # We must NOT iterate directly over candidates,
    # because that would return:
    #
    # candidate_1
    # candidate_2
    # candidate_3
    # ========================================================

    candidate_prompts = [

        candidates["candidate_1"],

        candidates["candidate_2"],

        candidates["candidate_3"]

    ]


    for index, candidate_prompt in enumerate(
        candidate_prompts,
        start=1
    ):

        prompts_to_test.append(
            {
                "name": f"Candidate {index}",
                "prompt": candidate_prompt
            }
        )


    # ========================================================
    # Debug:
    # Confirm exactly what will be evaluated
    # ========================================================

    print(
        "\nPROMPTS BEING EVALUATED:"
    )

    for prompt_data in prompts_to_test:

        print(
            f"\n{prompt_data['name']}"
        )

        print(
            "----------------------------------------"
        )

        print(
            prompt_data["prompt"]
        )


    # ========================================================
    # Step 6:
    # Execute every prompt against all scenarios
    # ========================================================

    all_results = []


    for prompt_data in prompts_to_test:

        print(
            f"\nExecuting "
            f"{prompt_data['name']}..."
        )


        batch_result = execute_prompt_batch(
            prompt_data["prompt"],
            scenarios
        )


        scenario_results = []


        for execution in batch_result[
            "results"
        ]:

            scenario_id = execution[
                "scenario_id"
            ]


            matching_scenario = next(
                (
                    scenario
                    for scenario in scenarios
                    if scenario["id"] == scenario_id
                ),
                None
            )


            if matching_scenario is None:

                raise ValueError(
                    f"No matching scenario found "
                    f"for scenario ID {scenario_id}."
                )


            scenario_results.append(
                {
                    "scenario_id": scenario_id,

                    "scenario": (
                        matching_scenario[
                            "description"
                        ]
                    ),

                    "generated_output": (
                        execution["output"]
                    )
                }
            )


        all_results.append(
            {
                "prompt_name": (
                    prompt_data["name"]
                ),

                "prompt": (
                    prompt_data["prompt"]
                ),

                "scenario_results": (
                    scenario_results
                ),

                "token_usage": (
                    batch_result[
                        "token_usage"
                    ]
                )
            }
        )


    print(
        "\nEvaluating all generated outputs..."
    )


    # ========================================================
    # Step 7:
    # Prepare evaluation items
    # ========================================================

    evaluation_items = []


    for prompt_result in all_results:

        for scenario_result in (
            prompt_result[
                "scenario_results"
            ]
        ):

            evaluation_items.append(
                {
                    "prompt_name": (
                        prompt_result[
                            "prompt_name"
                        ]
                    ),

                    "prompt": (
                        prompt_result[
                            "prompt"
                        ]
                    ),

                    "scenario_id": (
                        scenario_result[
                            "scenario_id"
                        ]
                    ),

                    "scenario": (
                        scenario_result[
                            "scenario"
                        ]
                    ),

                    "generated_output": (
                        scenario_result[
                            "generated_output"
                        ]
                    )
                }
            )


    # ========================================================
    # Step 8:
    # Evaluate generated outputs and prompts
    # ========================================================

    evaluation_response = judge_outputs_batch(
        user_prompt,
        task_analysis,
        evaluation_items,
        optimization_requirements
    )


    evaluations = evaluation_response[
        "evaluations"
    ]


    # ========================================================
    # Step 9:
    # Attach evaluation results to scenarios
    # ========================================================

    for evaluation in evaluations:

        matching_prompt_result = None


        for prompt_result in all_results:

            if (
                prompt_result[
                    "prompt_name"
                ]
                == evaluation[
                    "prompt_name"
                ]
            ):

                matching_prompt_result = (
                    prompt_result
                )

                break


        if matching_prompt_result is None:

            raise ValueError(
                "Evaluation returned an unknown "
                f"prompt name: "
                f"{evaluation['prompt_name']}"
            )


        matching_scenario_result = None


        for scenario_result in (
            matching_prompt_result[
                "scenario_results"
            ]
        ):

            if (
                scenario_result[
                    "scenario_id"
                ]
                == evaluation[
                    "scenario_id"
                ]
            ):

                matching_scenario_result = (
                    scenario_result
                )

                break


        if matching_scenario_result is None:

            raise ValueError(
                "Evaluation returned an unknown "
                f"scenario ID: "
                f"{evaluation['scenario_id']}"
            )


        matching_scenario_result[
            "output_quality_score"
        ] = evaluation[
            "output_quality_score"
        ]


        matching_scenario_result[
            "prompt_effectiveness_score"
        ] = evaluation[
            "prompt_effectiveness_score"
        ]


        matching_scenario_result[
            "overall_score"
        ] = evaluation[
            "overall_score"
        ]


        matching_scenario_result[
            "criterion_scores"
        ] = evaluation[
            "output_scores"
        ]


        matching_scenario_result[
            "prompt_effectiveness_scores"
        ] = evaluation[
            "prompt_effectiveness_scores"
        ]


        matching_scenario_result[
            "reasoning"
        ] = evaluation[
            "reasoning"
        ]


    # ========================================================
    # Step 10:
    # Calculate aggregate metrics
    # ========================================================

    number_of_scenarios = len(
        scenarios
    )


    if number_of_scenarios == 0:

        raise ValueError(
            "Cannot calculate metrics without scenarios."
        )


    for prompt_result in all_results:

        scenario_results = (
            prompt_result[
                "scenario_results"
            ]
        )


        if not scenario_results:

            raise ValueError(
                f"No scenario results found "
                f"for {prompt_result['prompt_name']}."
            )


        # ----------------------------------------------------
        # Average output quality
        # ----------------------------------------------------

        average_output_quality = sum(

            result[
                "output_quality_score"
            ]

            for result in scenario_results

        ) / len(scenario_results)


        prompt_result[
            "average_output_quality_score"
        ] = average_output_quality


        # ----------------------------------------------------
        # Average prompt effectiveness
        # ----------------------------------------------------

        average_prompt_effectiveness = sum(

            result[
                "prompt_effectiveness_score"
            ]

            for result in scenario_results

        ) / len(scenario_results)


        prompt_result[
            "average_prompt_effectiveness_score"
        ] = average_prompt_effectiveness


        # ----------------------------------------------------
        # Average overall score
        # ----------------------------------------------------

        average_overall_score = sum(

            result[
                "overall_score"
            ]

            for result in scenario_results

        ) / len(scenario_results)


        prompt_result[
            "average_overall_score"
        ] = average_overall_score


        # ----------------------------------------------------
        # Minimum output quality
        #
        # Measures worst-case scenario performance.
        # ----------------------------------------------------

        minimum_output_quality = min(

            result[
                "output_quality_score"
            ]

            for result in scenario_results

        )


        prompt_result[
            "minimum_output_quality_score"
        ] = minimum_output_quality


        # ----------------------------------------------------
        # Compatibility field
        # ----------------------------------------------------

        prompt_result[
            "average_quality_score"
        ] = average_overall_score


        # ----------------------------------------------------
        # Average token usage per scenario
        # ----------------------------------------------------

        prompt_result[
            "average_input_tokens"
        ] = (

            prompt_result[
                "token_usage"
            ][
                "input_tokens"
            ]

            / number_of_scenarios

        )


        prompt_result[
            "average_output_tokens"
        ] = (

            prompt_result[
                "token_usage"
            ][
                "output_tokens"
            ]

            / number_of_scenarios

        )


        prompt_result[
            "average_total_tokens"
        ] = (

            prompt_result[
                "token_usage"
            ][
                "total_tokens"
            ]

            / number_of_scenarios

        )


    # ========================================================
    # Step 11:
    # Select the best prompt
    #
    # Priority:
    #
    # 1. Highest average output quality
    # 2. Highest minimum output quality
    #    -> consistency
    # 3. Highest prompt effectiveness
    # 4. Lowest token usage
    #
    # Task performance is the primary objective.
    # ========================================================

    best_prompt = max(

        all_results,

        key=lambda result: (

            result[
                "average_output_quality_score"
            ],

            result[
                "minimum_output_quality_score"
            ],

            result[
                "average_prompt_effectiveness_score"
            ],

            -result[
                "average_total_tokens"
            ]

        )

    )


    # ========================================================
    # Step 12:
    # Selection explanation
    # ========================================================

    best_prompt[
        "selection_reason"
    ] = (

        "Selected based primarily on the highest "
        "average output quality across the evaluation "
        "scenarios. Scenario-level consistency was used "
        "as the next decision factor, followed by prompt "
        "effectiveness and token efficiency."

    )


    # ========================================================
    # Final result
    # ========================================================

    return {

        "task_analysis": task_analysis,

        "scenarios": scenarios,

        "results": all_results,

        "best_prompt": best_prompt

    }