# LLM evals with DeepEval

Six DeepEval tests grade the replies `reply()` in [support_bot.py](support_bot.py) drafts for support messages, with DeepEval's answer relevancy metric. Each test measures the metric itself instead of calling `assert_test`. It records the reply, the score and the threshold with `record_property`, which puts them in the JUnit XML.

The metric grades with `claude-sonnet-5-5`, a different model from the `claude-haiku-5-5` under test. The run stops when the two match.

## Run it locally

1. `cd deepeval`
2. `python -m venv .venv && source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. `export ANTHROPIC_API_KEY=<your key>`
5. `pytest tests/evals --junitxml=eval-results.xml`

`deepeval test run tests/evals --junitxml=eval-results.xml` works too. Without `ANTHROPIC_API_KEY`, the six tests skip and print why.

## The workflow

[deepeval.yml](../.github/workflows/deepeval.yml) runs on pull requests that change this folder and on every push to main. DeepEval test files are pytest files, so it runs plain `pytest`. It writes `eval-results.xml` and uploads it as the `eval-results` artifact, also when evals fail. `continue-on-error: true` keeps a failing eval from failing the job.

`junit_family = "xunit1"` in [pyproject.toml](pyproject.toml) keeps `record_property` values in the XML. It's set there, not with `-o`, because `deepeval test run` reads `-o` as its own flag.

[LLM evals with pytest in GitHub Actions](https://evalship.com/articles/llm-evals-with-pytest#deepeval) covers DeepEval in CI.
