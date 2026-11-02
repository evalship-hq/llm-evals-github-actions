import json

from openai import OpenAI

from support_bot import MODEL

# A model rates its own text higher, so the judge is another model, and the run stops if the two match.
JUDGE_MODEL = "gpt-6-sol"
if JUDGE_MODEL == MODEL:
    raise RuntimeError(f"The judge is {JUDGE_MODEL}, the model under test. Pick another judge.")

CRITERIA = {
    "answers_it": "The reply responds to what the customer asked or reported.",
    "no_promises": "The reply promises no refund, credit or fix date.",
    "next_step": "The reply tells the customer what happens next or what to do.",
}
PROMPT = (
    "You grade a support agent's reply to a customer message. Answer each criterion yes or no. Reply with JSON only: "
    '{"answers": {"<criterion id>": "yes" or "no"}, "reason": "<one sentence on each no>"}\n\nCriteria:\n'
    + "\n".join(f"{id}: {text}" for id, text in CRITERIA.items())
)


def grade(message: str, reply: str) -> dict:
    """Return the judge's yes or no for each criterion, and its reason."""
    client = OpenAI()
    response = client.chat.completions.create(
        model=JUDGE_MODEL,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": f"Customer message:\n{message}\n\nReply:\n{reply}"},
        ],
    )
    raw = response.choices[0].message.content or ""
    # A reply that doesn't parse, or misses a criterion, is never a pass: the test fails with what the judge said.
    try:
        verdict = json.loads(raw)
        answers = {id: str(verdict["answers"][id]).strip().lower() for id in CRITERIA}
        if not set(answers.values()) <= {"yes", "no"}:
            raise ValueError
    except (ValueError, KeyError, TypeError) as error:
        raise ValueError(f"Unreadable judge reply: {raw!r}") from error
    return {"answers": answers, "reason": str(verdict.get("reason", ""))}
