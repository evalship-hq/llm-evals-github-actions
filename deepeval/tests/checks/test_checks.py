# The code checks the evals run, tried on made-up replies. No model call, so CI runs these before the evals.
import pytest

from checks import states_support_hours, under_word_limit

RIGHT_HOURS = [
    "Our support team is available Monday to Friday, 9:00 to 17:00 CET.",
    "We're here Monday through Friday from 09:00 to 17:00 CET. Is there anything else I can help with?",
    "Support runs Mon–Fri, 9:00–17:00 (CET), though replies can take a few hours at busy times.",
    "You can reach us between 9:00 and 17:00 CET, Monday to Friday, so if you don't hear back today, we'll answer tomorrow.",
    "Hours: Monday-Friday, 9am to 5pm CET.",
]
WRONG_HOURS = [
    "",
    "What are your support hours?",  # the question echoed
    "I'm sorry, I can't share that.",
    "Our support team is available 24/7.",
    "Our support team is available Monday to Friday, 9:00 to 19:00 CET.",
    "Our support team is available Monday to Friday, 19:00 to 17:00 CET.",
    "Our support team is available Monday to Saturday, 9:00 to 17:00 CET.",
    "Our support team is available Monday to Friday, 9:00 to 17:00 EST.",
    "Our support team is available Monday to Friday, 9:00 to 17:00.",
    "We aren't open Monday to Friday, 9:00 to 17:00 CET anymore.",
    "Monday to Friday we answer email. Phones run 9:00 to 17:00 CET.",  # days and times in different sentences
]


@pytest.mark.parametrize("reply", RIGHT_HOURS)
def test_right_hours_pass(reply):
    assert states_support_hours(reply)


@pytest.mark.parametrize("reply", WRONG_HOURS)
def test_wrong_hours_fail(reply):
    assert not states_support_hours(reply)


def test_word_limit():
    assert under_word_limit("word " * 119)
    assert not under_word_limit("word " * 120)
    assert not under_word_limit("word " * 141)
