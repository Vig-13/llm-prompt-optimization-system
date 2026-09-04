from app.prompt_executor import execute_prompt


prompt_text = """
Write an email to a client about a project delay.
"""


scenario = """
You are a software project manager emailing a long-term corporate
client about a 4-day delay in delivering the beta version of a
custom mobile app due to unexpected API integration bugs.

Provide a revised delivery date and offer a brief status call.
"""


result = execute_prompt(
    prompt_text,
    scenario
)


print("\n" + "=" * 70)
print("GENERATED OUTPUT")
print("=" * 70)

print(result["output"])


print("\n" + "=" * 70)
print("TOKEN USAGE")
print("=" * 70)

print(
    f"Input Tokens: "
    f"{result['token_usage']['input_tokens']}"
)

print(
    f"Output Tokens: "
    f"{result['token_usage']['output_tokens']}"
)

print(
    f"Total Tokens: "
    f"{result['token_usage']['total_tokens']}"
)