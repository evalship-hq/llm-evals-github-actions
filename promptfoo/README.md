# LLM evals with promptfoo

[promptfooconfig.yaml](promptfooconfig.yaml) has six tests that check the model labels a support message as billing, bug or other. Each test has a `description`, so it keeps its name when you edit its message. The answer is trimmed and lowercased before the `equals` check.

## Run it locally

promptfoo needs Node.js 22.22 or later.

1. `cd promptfoo`
2. `export ANTHROPIC_API_KEY=<your key>`
3. `npx promptfoo@latest eval -c promptfooconfig.yaml --no-cache -o results.json`

Without `ANTHROPIC_API_KEY`, promptfoo stops and asks for it. The workflow checks for the key first and skips the evals with a notice.

## The workflow

[promptfoo.yml](../.github/workflows/promptfoo.yml) runs on pull requests that change this folder and on every push to main. It uploads `results.json` as the `eval-results` artifact, also when evals fail.

- `--no-cache` asks the model on every run. By default, promptfoo replays answers it cached on disk.
- promptfoo exits with code 100 when any test fails. `continue-on-error: true` keeps that from failing the job.

[Moving off OpenAI Evals: promptfoo in CI without flaky reds](https://evalship.com/articles/openai-evals-to-promptfoo) covers each setting and why.
