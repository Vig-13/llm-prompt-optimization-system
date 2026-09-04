from app.task_analyzer import analyze_task
from app.scenario_generator import generate_scenarios


user_prompt = """
Write an email to a client about a project delay.
"""


task_analysis = analyze_task(user_prompt)


scenarios = generate_scenarios(
    user_prompt,
    task_analysis
)


print("\n" + "=" * 70)
print("GENERATED SCENARIOS")
print("=" * 70)


for scenario in scenarios["scenarios"]:

    print(f"\nSCENARIO {scenario['id']}:")

    print(
        scenario["description"]
    )