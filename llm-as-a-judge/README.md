# LLM as a judge

Six pytest tests check the replies `reply()` in [support_bot.py](support_bot.py) drafts for support messages. Code in [checks.py](checks.py) checks the length, and the hours in the reply to the support-hours question. A judge in [judge.py](judge.py) grades the rest, with a yes or no for each of three criteria. Each test records the reply, the judge's answers and its reason with `record_property`, which puts them in the JUnit XML.

The judge avoids the mistakes in [LLM as a judge: five mistakes in real eval suites](https://evalship.com/articles/llm-as-a-judge-mistakes):

1. The judge is a different model from the one under test: `claude-sonnet-5-5` grades `claude-haiku-5-5`. The run stops when the two match.
2. The verdict comes from the criteria, in code. A judge reply that doesn't parse, or misses a criterion, fails the test.
3. The judge gets the customer's message, the reply and the criteria.
4. It grades the reply, not a whole conversation.
5. Code checks what code can: the 120-word limit and the support hours. The judge grades only what needs reading.

## Run it locally

1. `cd llm-as-a-judge`
2. `python -m venv .venv && source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. `export ANTHROPIC_API_KEY=<your key>`
5. `pytest tests/evals --junitxml=eval-results.xml`

Without `ANTHROPIC_API_KEY`, the six tests skip and print why. `pytest tests/checks` tries the code checks on made-up replies, with no model call. The workflow runs it before the evals.

## The workflow

[llm-as-a-judge.yml](../.github/workflows/llm-as-a-judge.yml) runs on pull requests that change this folder and on every push to main. It writes `eval-results.xml` and uploads it as the `eval-results` artifact, also when evals fail. `continue-on-error: true` keeps a failing eval from failing the job.

`junit_family = "xunit1"` in [pyproject.toml](pyproject.toml) keeps `record_property` values in the XML. The workflow passes it with `-o` too.
