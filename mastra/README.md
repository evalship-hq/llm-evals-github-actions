# LLM evals with Mastra

Six Vitest tests check that the Mastra agent in [support-agent.ts](support-agent.ts) labels a support message as billing, bug or other. Each test runs one item through Mastra's `expectEval` with a `checks.matches` gate. `test.for` names each test case by its id, so it keeps its name when you edit its message. Each test records the agent's answer with `annotate`, which the JUnit reporter writes as a property.

## Run it locally

1. `cd mastra`
2. `npm install`
3. `export ANTHROPIC_API_KEY=<your key>`
4. `npx vitest run evals`

Without `ANTHROPIC_API_KEY`, the six tests skip with a warning.

## The workflow

[mastra.yml](../.github/workflows/mastra.yml) runs on pull requests that change this folder and on every push to main. It runs Vitest with the default and JUnit reporters, so the log keeps its usual output. It uploads `eval-results.xml` as the `eval-results` artifact, also when evals fail. `continue-on-error: true` keeps a failing eval from failing the job.

The tests have no `retry`. A retried test that passes on its second try shows as a plain pass in the XML.

[Mastra evals on every pull request](https://evalship.com/articles/mastra-evals-in-ci) covers each setting and why.
