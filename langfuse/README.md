# Langfuse experiments in CI

[run_experiment.py](run_experiment.py) runs a Langfuse experiment over the `support-bot` dataset: `classify()` in [support_bot.py](support_bot.py) labels each support message as billing, bug or other. Next to reporting to Langfuse, it writes each test case's result to `eval-results.json`, in evalship's JSON format.

On its first run, the script creates the dataset from its six cases. After that, the dataset lives in Langfuse, and you edit it there. Each test case is known by its dataset item id.

## Run it locally

1. `cd langfuse`
2. `python -m venv .venv && source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. `export LANGFUSE_PUBLIC_KEY=<key> LANGFUSE_SECRET_KEY=<key> LANGFUSE_BASE_URL=https://cloud.langfuse.com ANTHROPIC_API_KEY=<key>`
5. `python run_experiment.py`

Without one of the keys, the script says which is missing and exits without running.

## The workflow

[langfuse.yml](../.github/workflows/langfuse.yml) runs on pull requests that change this folder and on every push to main. It uploads `eval-results.json` as the `eval-results` artifact, also when the script fails. It uses Langfuse's EU cloud; for the US cloud, set `LANGFUSE_BASE_URL` to `https://us.cloud.langfuse.com`.

The script fails a test case on its lowest score, and adds back cases whose task raised, which `run_experiment` leaves out.

[Langfuse experiments on every pull request](https://evalship.com/articles/langfuse-experiments-in-ci) covers the script and why.
