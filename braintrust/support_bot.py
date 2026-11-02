from openai import OpenAI

MODEL = "gpt-6-luna"
PROMPT = "Classify the customer support message as billing, bug or other. Reply with that one word only."


def classify(message: str) -> str:
    """Return billing, bug or other for a customer support message."""
    client = OpenAI()  # created here, not on import, so the evals can skip without a key
    reply = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": PROMPT}, {"role": "user", "content": message}],
    )
    return (reply.choices[0].message.content or "").strip().lower()
