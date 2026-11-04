# LangSmith evaluations in CI

[run_evaluation.py](run_evaluation.py) runs `client.evaluate()` over the `support-bot` dataset: `classify()` in [support_bot.py](support_bot.py) labels each support message as billing, bug or other. Next to reporting to LangSmith, it writes each example's result to `eval-results.json`, in evalship's JSON format.

On its first run, the script creates the dataset from its six cases. After that, the dataset lives in LangSmith, and you edit it there. Each example is known by its id.

## Run it locally

1. `cd langsmith`
2. `python -m venv .venv && source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. `export LANGSMITH_API_KEY=<key> ANTHROPIC_API_KEY=<key>`
5. `python run_evaluation.py`

Without one of the keys, the script says which is missing and exits without running.

## The workflow

[langsmith.yml](../.github/workflows/langsmith.yml) runs on pull requests that change this folder and on every push to main. It uploads `eval-results.json` as the `eval-results` artifact, also when the script fails.

With LangSmith's pytest, Vitest or Jest integration, your tests write JUnit XML as in the [pytest](../pytest), [vitest](../vitest) and [jest](../jest) folders. The guide covers what changes.

[LangSmith evaluations on every pull request](https://evalship.com/articles/langsmith-evals-in-ci) covers the script and why.
