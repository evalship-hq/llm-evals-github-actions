from anthropic import Anthropic

MODEL = "claude-haiku-5-5"
PROMPT = (
    "You answer customer support messages for a software product. Reply in under 120 words. "
    "Never promise a refund, credit or fix date: say who will follow up instead."
)


def reply(message: str) -> str:
    """Return a draft reply to a customer support message."""
    client = Anthropic()  # created here, not on import, so the evals can skip without a key
    response = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        system=PROMPT,
        messages=[{"role": "user", "content": message}],
    )
    # The model thinks first by default, so the reply is in the text blocks after its thinking block.
    return "".join(block.text for block in response.content if block.type == "text").strip()
