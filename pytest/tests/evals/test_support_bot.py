import os

import pytest

from support_bot import classify

pytestmark = pytest.mark.skipif(
    not os.environ.get("ANTHROPIC_API_KEY"), reason="ANTHROPIC_API_KEY is not set, so the evals can't call the model"
)

CASES = [
    pytest.param("I was charged twice for my subscription this month.", "billing", id="double-charge"),
    pytest.param("Can I get a refund for the annual plan I bought yesterday?", "billing", id="refund-request"),
    pytest.param("The app crashes every time I open the settings page.", "bug", id="app-crash"),
    pytest.param("Exporting a report to CSV fails with a 500 error.", "bug", id="export-error"),
    pytest.param("Could you add a dark mode?", "other", id="dark-mode"),
    pytest.param("What are your support hours?", "other", id="support-hours"),
]


@pytest.mark.parametrize("message, expected", CASES)
def test_classify(message, expected, record_property):
    label = classify(message)
    record_property("output", label)
    assert label == expected
