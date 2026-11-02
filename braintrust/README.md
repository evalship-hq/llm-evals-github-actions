# Braintrust evals in CI

[support_bot_eval.py](support_bot_eval.py) runs a Braintrust `Eval()` over six test cases: `classify()` in [support_bot.py](support_bot.py) labels each support message as billing, bug or other. Next to logging an experiment to Braintrust, it writes each test case's result to `eval-results.json`, in evalship's JSON format.

Each record's `metadata.id` is its key, so a test case keeps its history when you edit its message.

## Run it locally

1. `cd braintrust`
2. `python -m venv .venv && source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. `export BRAINTRUST_API_KEY=<key> OPENAI_API_KEY=<key>`
5. `python support_bot_eval.py`

Run it with `python`, not `braintrust eval`. Under `braintrust eval`, `Eval()` returns no results, so there's nothing to write. Without one of the keys, the script says which is missing and exits without running.

## The workflow

[braintrust.yml](../.github/workflows/braintrust.yml) runs on pull requests that change this folder and on every push to main. It uploads `eval-results.json` as the `eval-results` artifact, also when the script fails.

[Braintrust evals on every pull request](https://evalship.com/articles/braintrust-evals-in-ci) covers the script and why.
