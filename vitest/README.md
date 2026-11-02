# LLM evals with Vitest

Six Vitest tests check that `classify()` in [support-bot.ts](support-bot.ts) labels a support message as billing, bug or other. `test.for` names each test case by its id, so it keeps its name when you edit its message. Each test records the model's answer with `annotate`, which the JUnit reporter writes as a property.

## Run it locally

1. `cd vitest`
2. `npm install`
3. `export OPENAI_API_KEY=<your key>`
4. `npx vitest run evals`

Without `OPENAI_API_KEY`, the six tests skip with a warning.

## The workflow

[vitest.yml](../.github/workflows/vitest.yml) runs on pull requests that change this folder and on every push to main. It runs Vitest with the default and JUnit reporters, so the log keeps its usual output. It uploads `eval-results.xml` as the `eval-results` artifact, also when evals fail. `continue-on-error: true` keeps a failing eval from failing the job.

The tests have no `retry`. A retried test that passes on its second try shows as a plain pass in the XML.

[LLM evals with Vitest in GitHub Actions](https://evalship.com/articles/llm-evals-with-vitest) covers each setting and why.
