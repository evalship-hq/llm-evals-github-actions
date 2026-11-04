import os

import pytest
from deepeval.metrics import AnswerRelevancyMetric
from deepeval.models import AnthropicModel
from deepeval.test_case import LLMTestCase

from support_bot import MODEL, reply

pytestmark = pytest.mark.skipif(
    not os.environ.get("ANTHROPIC_API_KEY"), reason="ANTHROPIC_API_KEY is not set, so the evals can't call the model"
)

# A model rates its own text higher, so the metric grades with another model, and the run stops if the two match.
JUDGE_MODEL = "claude-sonnet-5-5"
if JUDGE_MODEL == MODEL:
    raise RuntimeError(f"The judge is {JUDGE_MODEL}, the model under test. Pick another judge.")

CASES = [
    pytest.param("I was charged twice for my subscription this month.", id="double-charge"),
    pytest.param("Can I get a refund for the annual plan I bought yesterday?", id="refund-request"),
    pytest.param("The app crashes every time I open the settings page.", id="app-crash"),
    pytest.param("Exporting a report to CSV fails with a 500 error.", id="export-error"),
    pytest.param("Could you add a dark mode?", id="dark-mode"),
    pytest.param("What are your support hours?", id="support-hours"),
]


@pytest.mark.parametrize("message", CASES)
def test_relevancy(message, record_property):
    case = LLMTestCase(input=message, actual_output=reply(message))
    record_property("output", case.actual_output)
    metric = AnswerRelevancyMetric(threshold=0.7, model=AnthropicModel(model=JUDGE_MODEL))  # built here, not on import: it needs the key
    # measure() and is_successful() instead of assert_test, so the score reaches the JUnit XML
    metric.measure(case)
    record_property("score", metric.score)
    record_property("threshold", metric.threshold)
    assert metric.is_successful(), metric.reason
