import os

import pytest

from checks import WORD_LIMIT, states_support_hours, under_word_limit
from judge import grade
from support_bot import reply

pytestmark = pytest.mark.skipif(
    not os.environ.get("ANTHROPIC_API_KEY"), reason="ANTHROPIC_API_KEY is not set, so the evals can't call the model"
)

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
def test_reply(message, record_property):
    answer = reply(message)
    record_property("output", answer)
    # Code checks what code can. The judge grades only the rest.
    assert under_word_limit(answer), f"{len(answer.split())} words, not under the {WORD_LIMIT} the prompt allows"
    if message == HOURS_QUESTION:
        assert states_support_hours(answer), "The reply doesn't give the hours in the prompt: Monday to Friday, 9:00 to 17:00 CET"

    verdict = grade(message, answer)
    for criterion, yes_or_no in verdict["answers"].items():
        record_property(criterion, yes_or_no)
    record_property("reason", verdict["reason"])
    # The verdict comes from the criteria, not from an overall pass the judge could get wrong.
    noes = [criterion for criterion, yes_or_no in verdict["answers"].items() if yes_or_no == "no"]
    assert not noes, f"The judge said no to {', '.join(noes)}: {verdict['reason']}"
