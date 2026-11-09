import os

import pytest
from deepeval.metrics import AnswerRelevancyMetric, GEval
from deepeval.models import AnthropicModel
from deepeval.test_case import LLMTestCase, SingleTurnParams

from checks import WORD_LIMIT, states_support_hours, under_word_limit
from support_bot import MODEL, reply

pytestmark = pytest.mark.skipif(
    not os.environ.get("ANTHROPIC_API_KEY"), reason="ANTHROPIC_API_KEY is not set, so the evals can't call the model"
)

# A model rates its own text higher, so the metric grades with another model, and the run stops if the two match.
JUDGE_MODEL = "claude-sonnet-5-5"
if JUDGE_MODEL == MODEL:
    raise RuntimeError(f"The judge is {JUDGE_MODEL}, the model under test. Pick another judge.")

HOURS_QUESTION = "What are your support hours?"
CASES = [
    pytest.param("I was charged twice for my subscription this month.", id="double-charge"),
    pytest.param("Can I get a refund for the annual plan I bought yesterday?", id="refund-request"),
    pytest.param("The app crashes every time I open the settings page.", id="app-crash"),
    pytest.param("Exporting a report to CSV fails with a 500 error.", id="export-error"),
    pytest.param("Could you add a dark mode?", id="dark-mode"),
    pytest.param(HOURS_QUESTION, id="support-hours"),
]


@pytest.mark.parametrize("message", CASES)
def test_relevancy(message, record_property):
    answer = reply(message)
    record_property("output", answer)
    # Code checks what code can, before any judge.
    assert under_word_limit(answer), f"{len(answer.split())} words, not under the {WORD_LIMIT} the prompt allows"
    if message == HOURS_QUESTION:
        assert states_support_hours(answer), "The reply doesn't give the hours in the prompt: Monday to Friday, 9:00 to 17:00 CET"

    judge = AnthropicModel(model=JUDGE_MODEL)  # built here, not on import: it needs the key
    case = LLMTestCase(input=message, actual_output=answer)
    # strict_mode makes the verdict pass or fail, with the judge's reason before it.
    no_promises = GEval(
        name="No promises",
        criteria="Fail if the reply promises a refund, a credit or a date for a fix. Pass if it promises none of them, "
        "for example by saying who will follow up instead.",
        evaluation_params=[SingleTurnParams.INPUT, SingleTurnParams.ACTUAL_OUTPUT],
        model=judge,
        strict_mode=True,
    )
    no_promises.measure(case)
    record_property("no_promises", no_promises.score)
    assert no_promises.is_successful(), no_promises.reason

    # measure() and is_successful() instead of assert_test, so the score reaches the JUnit XML
    relevancy = AnswerRelevancyMetric(threshold=0.7, model=judge)
    relevancy.measure(case)
    if message == HOURS_QUESTION:
        # A right answer here is three sentences, so relevancy turns on one of them (0.67 on 902cbff): the hours check
        # above decides this case, and its relevancy is only recorded.
        record_property("relevancy", relevancy.score)
        return
    record_property("score", relevancy.score)
    record_property("threshold", relevancy.threshold)
    assert relevancy.is_successful(), relevancy.reason
