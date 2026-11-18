"""
Turning two numbers into one, and one number into something a person can read.
(Built in Milestones 4 and 5.)

Two functions live here.

`combine_signals` is where your false-positive decision from Milestone 1
actually gets made. Everything above it — the labels, the appeal path — is
downstream of a number this function produced.

`score_to_label` is where you stop writing for a machine and start writing for
a person. A score of 0.62 means nothing to a writer.

⚠️ Your README's **Signals and Scoring** section has to name the file and
function holding your combining rule. The grader checks your code against what
you claim, so that line should read `scoring.py::combine_signals`.
"""

import config


def combine_signals(model_score: float, style_score: float) -> float:
    """
    Combine two 0–1 signals into one 0–1 score (higher = more likely AI).

    The rule:
      1. Weighted average: 0.6 * model_score + 0.4 * style_score
         (weights in config.py).
      2. Disagreement rule: if the two signals are more than 0.4 apart
         (config.DISAGREEMENT_GAP), the result is clamped into the unsure band
         [HUMAN_THRESHOLD + 0.01, AI_THRESHOLD - 0.01]. When two different methods
         disagree that strongly, the honest answer is "unsure", and one signal
         on its own can never put a writer in the AI band.
    """
    combined = (
        config.WEIGHT_MODEL_SIGNAL * model_score
        + config.WEIGHT_STYLE_SIGNAL * style_score
    )
    if abs(model_score - style_score) > config.DISAGREEMENT_GAP:
        combined = min(max(combined, config.HUMAN_THRESHOLD + 0.01),
                       config.AI_THRESHOLD - 0.01)
    return round(min(max(combined, 0.0), 1.0), 4)


LABEL_AI = (
    "This piece reads very much like text written by an AI tool. "
    "This is an automated guess, not proof, and it can be wrong. "
    "If you wrote it yourself, you can appeal and a person will review it."
)
LABEL_HUMAN = "We think this was written by a person."
LABEL_UNSURE = (
    "Our automated check couldn't tell whether this was written by a person "
    "or with an AI tool. That happens often with ordinary writing, and it is "
    "not an accusation. If you'd like a person to look at it, you can ask for "
    "a review."
)


def score_to_label(score: float) -> tuple[str, str]:
    """
    Turn a score into (guess, label_text).

        score >= AI_THRESHOLD     -> "ai"      LABEL_AI
        score <= HUMAN_THRESHOLD  -> "human"   LABEL_HUMAN
        anything in between       -> "unsure"  LABEL_UNSURE

    Every score from 0.0 to 1.0 lands in exactly one branch, so there are no gaps.
    """
    if score >= config.AI_THRESHOLD:
        return "ai", LABEL_AI
    if score <= config.HUMAN_THRESHOLD:
        return "human", LABEL_HUMAN
    return "unsure", LABEL_UNSURE


def label_ranges() -> list[tuple[str, str]]:
    """
    The score range each label covers. Your README needs these beside the
    label text — given to you so the numbers can't drift apart from config.py.
    """
    return [
        ("high-confidence human", f"0.00 – {config.HUMAN_THRESHOLD:.2f}"),
        ("unsure", f"{config.HUMAN_THRESHOLD:.2f} – {config.AI_THRESHOLD:.2f}"),
        ("high-confidence AI", f"{config.AI_THRESHOLD:.2f} – 1.00"),
    ]