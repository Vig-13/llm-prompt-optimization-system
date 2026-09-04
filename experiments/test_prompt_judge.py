from app.task_analyzer import analyze_task
from app.scenario_generator import generate_scenarios
from app.prompt_executor import execute_prompt
from app.prompt_judge import judge_output


user_prompt = """
Write an email to a client about a project delay.
"""


task_analysis = analyze_task(user_prompt)


scenarios = generate_scenarios(
    user_prompt,
    task_analysis
)


scenario = scenarios["scenarios"][0]["description"]


result = execute_prompt(
    user_prompt,
    scenario
)


evaluation = judge_output(
    user_prompt,
    task_analysis,
    scenario,
    result["output"]
)


print("\n" + "=" * 70)
print("GENERATED OUTPUT")
print("=" * 70)

print(result["output"])


print("\n" + "=" * 70)
print("EVALUATION")
print("=" * 70)


for item in evaluation["scores"]:

    print(
        f"{item['criterion']}: "
        f"{item['score']}"
    )


print("\nOverall Score:")

print(
    evaluation["overall_score"]
)


print("\nReasoning:")

print(
    evaluation["reasoning"]
)