# LLM evals with pytest

Six pytest tests check that `classify()` in [support_bot.py](support_bot.py) labels a support message as billing, bug or other. Each test case has an id, so it keeps its name when you edit its message. Each test records the model's answer with `record_property`, which puts it in the JUnit XML.

## Run it locally

1. `cd pytest`
2. `python -m venv .venv && source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. `export OPENAI_API_KEY=<your key>`
5. `pytest tests/evals --junitxml=eval-results.xml`

Without `OPENAI_API_KEY`, the six tests skip and print why.

## The workflow

[pytest.yml](../.github/workflows/pytest.yml) runs on pull requests that change this folder and on every push to main. It writes `eval-results.xml` and uploads it as the `eval-results` artifact, also when evals fail. `continue-on-error: true` keeps a failing eval from failing the job.

`junit_family = "xunit1"` in [pyproject.toml](pyproject.toml) keeps `record_property` values in the XML. The workflow passes it with `-o` too.

[LLM evals with pytest in GitHub Actions](https://evalship.com/articles/llm-evals-with-pytest) covers each setting and why.
