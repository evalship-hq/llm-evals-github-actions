# LLM evals with Jest

Six Jest tests check that `classify()` in [support-bot.js](support-bot.js) labels a support message as billing, bug or other. `test.each` names each test case by its id, so it keeps its name when you edit its message.

Jest can't attach data to a test's result, so three small files put the model's answer in the JUnit XML:

- [evals/record.js](evals/record.js): a test calls `record({ output })`, which appends to a side file.
- [junitTestCaseProperties.js](junitTestCaseProperties.js): jest-junit reads the side file and adds each test's properties.
- [jest.global-setup.js](jest.global-setup.js): clears the side file before each run.

## Run it locally

1. `cd jest`
2. `npm install`
3. `export ANTHROPIC_API_KEY=<your key>`
4. `npx jest evals`

Without `ANTHROPIC_API_KEY`, the six tests skip with a warning.

## The workflow

[jest.yml](../.github/workflows/jest.yml) runs on pull requests that change this folder and on every push to main. It writes `eval-results.xml` with jest-junit and uploads it as the `eval-results` artifact, also when evals fail. `continue-on-error: true` keeps a failing eval from failing the job.

The five `JEST_JUNIT_*` settings in the workflow name each test by its describe block and title, in a suite named after its file.

[LLM evals with Jest in GitHub Actions](https://evalship.com/articles/llm-evals-with-jest) covers each setting and why.
