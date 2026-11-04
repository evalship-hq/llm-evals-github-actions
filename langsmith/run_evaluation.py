import json
import os
import sys

from langsmith import Client

from support_bot import classify

KEYS = ["LANGSMITH_API_KEY", "ANTHROPIC_API_KEY"]
if missing := [k for k in KEYS if not os.environ.get(k)]:
    print(f"Skipping the evaluation: {', '.join(missing)} not set.")
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
client = Client()

if not client.has_dataset(dataset_name=DATASET):  # first run: create it from CASES; after that, LangSmith keeps it
    client.create_dataset(DATASET)
    client.create_examples(dataset_name=DATASET, examples=[
        {"inputs": {"message": message}, "outputs": {"label": label}} for message, label in CASES])


def target(inputs: dict) -> dict:
    return {"label": classify(inputs["message"])}


def exact(outputs: dict, reference_outputs: dict) -> bool:
    return outputs["label"] == reference_outputs["label"]


results = client.evaluate(target, data=DATASET, evaluators=[exact], experiment_prefix="ci")

evals = []
for row in results:
    run, example = row["run"], row["example"]
    scores = [float(e.score) for e in row["evaluation_results"]["results"] if e.score is not None]
    score = min(scores) if scores else None
    evals.append({"key": str(example.id), "score": score, "threshold": THRESHOLD,
                  "passed": run.error is None and score is not None and score >= THRESHOLD,
                  "failure": run.error, "input": example.inputs, "output": run.outputs,
                  "url": run.get_url()})

# One suite per folder, so the seven tools in this repository stay apart in evalship.
json.dump({"schema": "evalship/v1", "suite": "langsmith", "url": results.url, "evals": evals},
          open("eval-results.json", "w"), default=str)
