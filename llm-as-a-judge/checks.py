import re

WORD_LIMIT = 120  # the prompt in support_bot.py says "under 120 words"
DAYS = r"\bmon(day)?\s*(to|through|until|-|–|—)\s*fri(day)?\b"
TIME = r"(?<![\d:])0?9(:00)?\s*(am)?\s*(to|until|and|-|–|—)\s*(17:00|5(:00)?\s*pm)(?![\d:])"
NEGATION = r"\b(not|never|no longer|closed)\b|n['’]t"


def under_word_limit(reply: str) -> bool:
    return len(reply.split()) < WORD_LIMIT


def states_support_hours(reply: str) -> bool:
    """True when one sentence gives the hours in support_bot.py's prompt: Monday to Friday, 9:00 to 17:00 CET."""
    # shortcut: a negation in the same clause before the hours ("we aren't open Monday to Friday ...") fails it, one after doesn't
    for sentence in re.split(r"(?<=[.!?;])\s+", reply.lower()):
        days, time = re.search(DAYS, sentence), re.search(TIME, sentence)
        if days and time and re.search(r"\bcet\b", sentence) and not re.search(NEGATION, sentence[: min(days.start(), time.start())]):
            return True
    return False
