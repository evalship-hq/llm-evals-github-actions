# Run LLM evals in GitHub Actions on every pull request

The first seven folders run the same evals with a different tool. The prompt classifies a customer support message as billing, bug or other, and six test cases check it. In the last two, the support bot drafts a reply to the same six messages, and an LLM judge grades it. Each folder has its own workflow in [.github/workflows](.github/workflows).

| Folder | Results file | Secrets | Guide |
|---|---|---|---|
| [pytest](pytest) | JUnit XML, `eval-results.xml` | `ANTHROPIC_API_KEY` | [LLM evals with pytest in GitHub Actions](https://evalship.com/articles/llm-evals-with-pytest) |
| [vitest](vitest) | JUnit XML, `eval-results.xml` | `ANTHROPIC_API_KEY` | [LLM evals with Vitest in GitHub Actions](https://evalship.com/articles/llm-evals-with-vitest) |
| [jest](jest) | JUnit XML, `eval-results.xml` | `ANTHROPIC_API_KEY` | [LLM evals with Jest in GitHub Actions](https://evalship.com/articles/llm-evals-with-jest) |
| [promptfoo](promptfoo) | promptfoo JSON, `results.json` | `ANTHROPIC_API_KEY` | [Replacing OpenAI Evals: promptfoo in CI without flaky reds](https://evalship.com/articles/openai-evals-to-promptfoo) |
| [langfuse](langfuse) | evalship JSON, `eval-results.json` | `ANTHROPIC_API_KEY`, `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY` | [Langfuse experiments on every pull request](https://evalship.com/articles/langfuse-experiments-in-ci) |
| [braintrust](braintrust) | evalship JSON, `eval-results.json` | `ANTHROPIC_API_KEY`, `BRAINTRUST_API_KEY` | [Braintrust evals on every pull request](https://evalship.com/articles/braintrust-evals-in-ci) |
| [langsmith](langsmith) | evalship JSON, `eval-results.json` | `ANTHROPIC_API_KEY`, `LANGSMITH_API_KEY` | [LangSmith evaluations on every pull request](https://evalship.com/articles/langsmith-evals-in-ci) |
| [deepeval](deepeval) | JUnit XML, `eval-results.xml` | `ANTHROPIC_API_KEY` | [LLM evals with pytest in GitHub Actions: DeepEval](https://evalship.com/articles/llm-evals-with-pytest#deepeval) |
| [llm-as-a-judge](llm-as-a-judge) | JUnit XML, `eval-results.xml` | `ANTHROPIC_API_KEY` | [LLM as a judge: five mistakes in real eval suites](https://evalship.com/articles/llm-as-a-judge-mistakes) |

To choose a tool, see [LLM evals on pull requests: how the tools compare](https://evalship.com/articles/llm-evals-on-pull-requests).

## What every workflow does

- It runs on pull requests that change its folder or its workflow file, and on every push to main. The runs on main give each pull request results to compare with.
- It uploads the results file as the `eval-results` artifact. The upload has `if: always()`, so it also runs when evals fail.
- A failing eval doesn't fail the job. LLM evals fail by chance now and then, and one such failure shouldn't block a merge.
- Without the secrets it needs, it skips the evals and stays green. Pull requests from forks get no secrets, so their evals skip.

## Use one in your repository

1. Copy the tool's folder and its workflow file.
2. In the workflow, change `working-directory`, `paths` and the upload `path` to where you put the folder.
3. Add the secrets from the table under **Settings** > **Secrets and variables** > **Actions**.
4. Replace the prompt in the support bot file and the test cases with your own.

## What evalship adds

[evalship](https://evalship.com) is a GitHub App that reads the results file these workflows upload. On each pull request, it comments with the test cases the change broke compared with main, and whether a failure looks flaky.
