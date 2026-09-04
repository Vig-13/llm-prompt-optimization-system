from app.candidate_generator import generate_candidates
user_prompt = """
Write an email to a client about a project delay.
"""


desired_outcome = """
The email should be professional and reassuring.
It should explain the delay without sounding defensive,
provide a revised timeline, and maintain client trust.
"""


candidates = generate_candidates(
    user_prompt,
    desired_outcome
)


print("\n" + "=" * 70)
print("PROMPT CANDIDATES")
print("=" * 70)


print("\nCANDIDATE 1:\n")
print(candidates["candidate_1"])


print("\nCANDIDATE 2:\n")
print(candidates["candidate_2"])


print("\nCANDIDATE 3:\n")
print(candidates["candidate_3"])