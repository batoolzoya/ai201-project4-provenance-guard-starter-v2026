"""
Signal two: the style signal. (Built in Milestone 4.)

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three measures ────────────────────────────────────────────────────────
#
# Each measure returns a raw number. style_signal() below turns each into a
# 0–1 "AI-likeness" and averages them with fixed weights.

# Marks that vary a lot between writers. Full stops and commas are left out on
# purpose: almost everyone uses them, so they say little about who wrote it.
EXPRESSIVE_PUNCTUATION = set(";:—–-()!?\"…")


def sentence_length_spread(text: str) -> float | None:
    """
    Coefficient of variation of sentence length: stdev(words per sentence)
    divided by mean(words per sentence).

    Scale: 0 = every sentence the same length; ~0.6+ = very uneven.
    Direction: HIGHER = more human-like (lumpier).
    Edge case: fewer than 2 sentences has no spread to measure, so it returns
    None and style_signal treats this measure as neutral (0.5).
    """
    lengths = [len(words(s)) for s in sentences(text)]
    lengths = [n for n in lengths if n > 0]
    if len(lengths) < 2:
        return None
    mean = statistics.mean(lengths)
    return round(statistics.stdev(lengths) / mean, 4) if mean else None


def type_token_ratio(text: str, window: int = 50) -> float:
    """
    Moving-average type-token ratio (MATTR): unique/total words inside every
    50-word window, averaged. Plain TTR falls as text gets longer, so the
    window keeps a long piece and a short piece comparable. Texts under 50
    words fall back to plain TTR.

    Scale: 0–1. Direction: HIGHER = more varied vocabulary = more human-like.
    """
    tokens = words(text)
    if not tokens:
        return 0.0
    if len(tokens) <= window:
        return round(len(set(tokens)) / len(tokens), 4)
    ratios = [
        len(set(tokens[i:i + window])) / window
        for i in range(len(tokens) - window + 1)
    ]
    return round(sum(ratios) / len(ratios), 4)


def punctuation_density(text: str) -> float:
    """
    Expressive punctuation per sentence: ; : dashes brackets ! ? quotes and
    ellipses, divided by the number of sentences.

    Scale: 0 = none; 1.0 = about one such mark per sentence.
    Direction: HIGHER = more human-like.
    """
    count = sum(1 for ch in text if ch in EXPRESSIVE_PUNCTUATION)
    n_sentences = max(len(sentences(text)), 1)
    return round(count / n_sentences, 4)


# ── Combining them ───────────────────────────────────────────────────────────

# Each raw measure is mapped onto 0–1 AI-likeness with a straight line between
# two anchor points, then clamped. Anchors are the raw value that counts as
# fully AI-like (score 1.0) and fully human-like (score 0.0).
SPREAD_AI, SPREAD_HUMAN = 0.15, 0.65   # coefficient of variation
TTR_AI, TTR_HUMAN = 0.60, 0.85         # MATTR
PUNCT_AI, PUNCT_HUMAN = 0.0, 0.8       # expressive marks per sentence

STYLE_WEIGHTS = {"spread": 0.4, "ttr": 0.3, "punct": 0.3}


def _ai_likeness(value: float | None, ai_anchor: float, human_anchor: float) -> float:
    """Map a raw measure to 0–1 where 1 = AI-like. None -> neutral 0.5."""
    if value is None:
        return 0.5
    score = (human_anchor - value) / (human_anchor - ai_anchor)
    return min(max(score, 0.0), 1.0)


def style_parts(text: str) -> dict:
    """Every raw measure and its 0–1 AI-likeness — handy for diagnosis."""
    spread = sentence_length_spread(text)
    ttr = type_token_ratio(text)
    punct = punctuation_density(text)
    return {
        "spread_raw": spread,
        "ttr_raw": ttr,
        "punct_raw": punct,
        "spread_ai": round(_ai_likeness(spread, SPREAD_AI, SPREAD_HUMAN), 4),
        "ttr_ai": round(_ai_likeness(ttr, TTR_AI, TTR_HUMAN), 4),
        "punct_ai": round(_ai_likeness(punct, PUNCT_AI, PUNCT_HUMAN), 4),
    }


def style_signal(text: str) -> float:
    """
    The style signal as a 0–1 score. **Higher means more likely AI.**

    All three measures point the "human" way when they are high, so each is
    flipped by _ai_likeness, then combined:

        style = 0.4 * spread_ai + 0.3 * ttr_ai + 0.3 * punct_ai

    Sentence-length spread gets the most weight because it is the measure the
    human/AI difference is most often described in; the other two are noisier.
    """
    parts = style_parts(text)
    score = (
        STYLE_WEIGHTS["spread"] * parts["spread_ai"]
        + STYLE_WEIGHTS["ttr"] * parts["ttr_ai"]
        + STYLE_WEIGHTS["punct"] * parts["punct_ai"]
    )
    return round(min(max(score, 0.0), 1.0), 4)


if __name__ == "__main__":
    import sys

    sys.stdout.reconfigure(encoding="utf-8")

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
