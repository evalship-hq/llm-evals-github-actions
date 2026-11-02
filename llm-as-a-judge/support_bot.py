from openai import OpenAI

MODEL = "gpt-6-luna"
PROMPT = (
    "You answer customer support messages for a software product. Reply in under 120 words. "
    "Never promise a refund, credit or fix date: say who will follow up instead."
)


def reply(message: str) -> str:
    """Return a draft reply to a customer support message."""
    client = OpenAI()  # created here, not on import, so the evals can skip without a key
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": PROMPT}, {"role": "user", "content": message}],
    )
    return (response.choices[0].message.content or "").strip()
