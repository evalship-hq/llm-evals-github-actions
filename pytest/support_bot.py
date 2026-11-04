from anthropic import Anthropic

MODEL = "claude-haiku-5-5"
PROMPT = "Classify the customer support message as billing, bug or other. Reply with that one word only."


def classify(message: str) -> str:
    """Return billing, bug or other for a customer support message."""
    client = Anthropic()  # created here, not on import, so the evals can skip without a key
    reply = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        system=PROMPT,
        messages=[{"role": "user", "content": message}],
    )
    # The model thinks first by default, so the answer is in the text blocks after its thinking block.
    return "".join(block.text for block in reply.content if block.type == "text").strip().lower()
