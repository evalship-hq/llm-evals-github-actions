## Evals
When you change a prompt, a model or an LLM call, add or update a test case for the change in that folder's suite and try it with its command, run from the folder:
- pytest: `pytest/tests/evals/test_support_bot.py`, `pytest tests/evals`
- vitest: `vitest/evals/support-bot.test.ts`, `npx vitest run evals`
- jest: `jest/evals/support-bot.test.js`, `npx jest evals`
- promptfoo: `promptfoo/promptfooconfig.yaml`, `npx promptfoo@0.125.1 eval -c promptfooconfig.yaml --no-cache`
- deepeval: `deepeval/tests/evals/test_support_bot.py`, `pytest tests/checks tests/evals`
- llm-as-a-judge: `llm-as-a-judge/tests/evals/test_support_bot.py`, `pytest tests/checks tests/evals`
- braintrust: `braintrust/support_bot_eval.py`, `python support_bot_eval.py`
- langsmith: `langsmith/run_evaluation.py`, `python run_evaluation.py`
- langfuse: `langfuse/run_experiment.py`, `python run_experiment.py`

Before you finish, run the evals the change affects, as you would its tests: follow https://evalship.com/change.md?repo=evalship-hq/llm-evals-github-actions, which sends evalship the change's diff with its results.
