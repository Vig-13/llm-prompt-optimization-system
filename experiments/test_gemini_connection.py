from app.generator import client


response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents="Say hello in one sentence."
)

print(response.text)