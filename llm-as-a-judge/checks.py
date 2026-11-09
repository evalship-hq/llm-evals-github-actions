import re

WORD_LIMIT = 120  # the prompt in support_bot.py says "under 120 words"
DAYS = r"\bmon(day)?\s*(to|through|until|-|–|—)\s*fri(day)?\b"
TIME = r"(?<![\d:])0?9(:00)?\s*(am)?\s*(to|until|and|-|–|—)\s*(17:00|5(:00)?\s*(pm)?)(?![\d:])"
NEGATION = r"\b(not|never|no longer|closed)\b|n['’]t"
CLOCK = r"(?<![\d:])(\d{1,2})(?::(\d\d))?\s*(am|pm)\b|(?<![\d:])(\d{1,2}):(\d\d)(?![\d:])"
ALWAYS = r"24/7|24 hours|round the clock"


def under_word_limit(reply: str) -> bool:
    return len(reply.split()) < WORD_LIMIT


def states_support_hours(reply: str) -> bool:
    """True when a sentence gives the hours in support_bot.py's prompt, Monday to Friday, 9:00 to 17:00 CET, and no other hours."""
    text = reply.lower().replace("a.m.", "am").replace("p.m.", "pm")
    # Any other time of day, or 24/7, contradicts the prompt's hours, wherever it is in the reply.
    for hour, minutes, half, hour24, minutes24 in re.findall(CLOCK, text):
        h = int(hour or hour24)
        h += 12 if half == "pm" and h < 12 else 0
        if h not in (9, 17) or (minutes or minutes24 or "00") != "00":
            return False
    if re.search(ALWAYS, text):
        return False
    # shortcut: a negation in the same clause before the hours ("we aren't open Monday to Friday ...") fails it, one after
    # doesn't; other days with no time ("we're also open on Saturdays") pass
    for sentence in re.split(r"(?<=[.!?;])\s+", text):
        days, time = re.search(DAYS, sentence), re.search(TIME, sentence)
        if days and time and re.search(r"\bcet\b", sentence) and not re.search(NEGATION, sentence[: min(days.start(), time.start())]):
            return True
    return False
