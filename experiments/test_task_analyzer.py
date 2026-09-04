from app.task_analyzer import analyze_task


user_prompt = """
Write an email to a client about a project delay.
"""


result = analyze_task(user_prompt)


print("\n" + "=" * 70)
print("TASK ANALYSIS")
print("=" * 70)

print("\nTask Type:")
print(result["task_type"])

print("\nTask Summary:")
print(result["task_summary"])

print("\nExpected Output:")
print(result["expected_output"])

print("\nEvaluation Focus:")

for item in result["evaluation_focus"]:
    print(f"- {item}")