import json
import os
import sys

from braintrust import Eval

from support_bot import classify

KEYS = ["BRAINTRUST_API_KEY", "ANTHROPIC_API_KEY"]
if missing := [k for k in KEYS if not os.environ.get(k)]:
    print(f"Skipping the eval: {', '.join(missing)} not set.")
    sys.exit(0)

# Each record's metadata id is its key in evalship, so it keeps its history when you edit the message.
DATA = [
    {"input": "I was charged twice for my subscription this month.", "expected": "billing", "metadata": {"id": "double-charge"}},
    {"input": "Can I get a refund for the annual plan I bought yesterday?", "expected": "billing", "metadata": {"id": "refund-request"}},
    {"input": "The app crashes every time I open the settings page.", "expected": "bug", "metadata": {"id": "app-crash"}},
    {"input": "Exporting a report to CSV fails with a 500 error.", "expected": "bug", "metadata": {"id": "export-error"}},
    {"input": "Could you add a dark mode?", "expected": "other", "metadata": {"id": "dark-mode"}},
    {"input": "What are your support hours?", "expected": "other", "metadata": {"id": "support-hours"}},
]
THRESHOLD = 0.8


def task(input, hooks):
    hooks.metadata["trace_url"] = hooks.span.link()  # this test case's trace in Braintrust
    return classify(input)


def exact(input, output, expected):
    return 1.0 if output == expected else 0.0


result = Eval("support-bot", data=DATA, task=task, scores=[exact])

evals = []
for r in result.results:
    scores = [s for s in r.scores.values() if s is not None]
    score = min(scores) if scores else None
    evals.append({"key": (r.origin or {}).get("id") or r.metadata["id"], "score": score, "threshold": THRESHOLD,
                  "passed": r.error is None and score is not None and score >= THRESHOLD,
                  "failure": str(r.error) if r.error else None,
                  "input": r.input, "output": r.output, "url": r.metadata.get("trace_url")})

# One suite per folder, so the seven tools in this repository stay apart in evalship.
json.dump({"schema": "evalship/v1", "suite": "braintrust", "url": result.summary.experiment_url, "evals": evals},
          open("eval-results.json", "w"), default=str)
