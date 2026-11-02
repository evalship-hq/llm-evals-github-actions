import json
import os
import sys

from langfuse import Evaluation, get_client
from langfuse.api import NotFoundError

from support_bot import classify

KEYS = ["LANGFUSE_PUBLIC_KEY", "LANGFUSE_SECRET_KEY", "OPENAI_API_KEY"]
if missing := [k for k in KEYS if not os.environ.get(k)]:
    print(f"Skipping the experiment: {', '.join(missing)} not set.")
    sys.exit(0)

DATASET = "support-bot"
CASES = [
    ("I was charged twice for my subscription this month.", "billing"),
    ("Can I get a refund for the annual plan I bought yesterday?", "billing"),
    ("The app crashes every time I open the settings page.", "bug"),
    ("Exporting a report to CSV fails with a 500 error.", "bug"),
    ("Could you add a dark mode?", "other"),
    ("What are your support hours?", "other"),
]
THRESHOLD = 0.8
langfuse = get_client()


def get_dataset():
    try:
        return langfuse.get_dataset(DATASET)
    except NotFoundError:  # first run: create it from CASES; after that, Langfuse keeps the dataset
        langfuse.create_dataset(name=DATASET)
        for message, label in CASES:
            langfuse.create_dataset_item(dataset_name=DATASET, input=message, expected_output=label)
        return langfuse.get_dataset(DATASET)


def task(*, item, **kwargs):
    return classify(item.input)


def exact(*, output, expected_output, **kwargs):
    return Evaluation(name="exact", value=float(output == expected_output))


def trace_url(trace_id):
    try:
        return langfuse.get_trace_url(trace_id=trace_id)
    except Exception:  # a missing link shouldn't fail the run
        return None


dataset = get_dataset()
result = dataset.run_experiment(name="ci", task=task, evaluators=[exact])

evals, ran = [], set()
for r in result.item_results:
    ran.add(r.item.id)
    scores = [e.value for e in r.evaluations if isinstance(e.value, (int, float))]
    score = min(scores) if scores else None
    evals.append({"key": r.item.id, "score": score, "threshold": THRESHOLD,
                  "passed": score is not None and score >= THRESHOLD,
                  "input": r.item.input, "output": r.output, "url": trace_url(r.trace_id)})
# run_experiment leaves out items whose task raised, so add them back as failures
evals += [{"key": item.id, "passed": False, "input": item.input, "failure": "The task raised an error."}
          for item in dataset.items if item.id not in ran]

# One suite per folder, so the seven tools in this repository stay apart in evalship.
json.dump({"schema": "evalship/v1", "suite": "langfuse", "url": result.experiment_url, "evals": evals},
          open("eval-results.json", "w"), default=str)
