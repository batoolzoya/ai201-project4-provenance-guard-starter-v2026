#!/usr/bin/env python3
"""
Score a set of inputs through the running service and print one table.

    python app.py              # terminal 1
    python try_inputs.py       # terminal 2

Used for the Milestone 4 calibration inputs (clearly AI, lightly-edited AI,
and my own writing). My own writing is read from private/my_writing.txt,
which is git-ignored: pieces are separated by a line containing only ---.
Only piece numbers and scores are printed, never the text itself.

    python try_inputs.py private\\extra.txt    # score only the pieces in another file
"""

import sys
from pathlib import Path

import requests

sys.stdout.reconfigure(encoding="utf-8")

URL = "http://127.0.0.1:5000/submit"
PRIVATE = Path(__file__).parent / "private" / "my_writing.txt"

# AI-generated text (written by Claude for testing).
AI_CLEAR = (
    "Time management is an essential skill for students who want to succeed "
    "academically. By creating a schedule and prioritizing tasks, students can "
    "reduce stress and improve their overall performance. Additionally, it is "
    "important to take regular breaks to maintain focus and productivity. "
    "Ultimately, developing good time management habits can lead to long-term "
    "success in both school and life."
)
# The same AI text, lightly edited: contractions, a dash, a lowercase slip,
# one sentence split up.
AI_EDITED = (
    "Time management is a skill every student needs. If you make a schedule "
    "and put the big tasks first, you'll feel less stressed. You'll do better "
    "too. Taking breaks matters - it helps you stay focused. honestly, good "
    "habits now pay off later, in school and after."
)


def my_pieces(path=PRIVATE):
    if not path.exists():
        print(f"(no {path} — skipping)")
        return []
    raw = path.read_text(encoding="utf-8-sig")
    return [p.strip() for p in raw.split("\n---") if p.strip().strip("-").strip()]


def main():
    if len(sys.argv) > 1:
        extra = Path(sys.argv[1])
        inputs = [(f"{extra.stem} #{i}", t) for i, t in enumerate(my_pieces(extra), 1)]
    else:
        inputs = [("clearly AI", AI_CLEAR), ("lightly-edited AI", AI_EDITED)]
        inputs += [(f"my piece #{i}", t) for i, t in enumerate(my_pieces(), 1)]

    print(f"{'input':<20}{'words':>6}{'model':>8}{'style':>8}{'combined':>10}  guess")
    print("-" * 62)
    for name, text in inputs:
        r = requests.post(URL, json={"text": text, "creator_id": "zoya_calibration"},
                          timeout=120)
        d = r.json()
        if r.status_code != 200:
            print(f"{name:<20}{len(text.split()):>6}  HTTP {r.status_code} {d.get('error')}")
            continue
        print(f"{name:<20}{len(text.split()):>6}{d['model_score']:>8.3f}"
              f"{d['style_score']:>8.3f}{d['confidence']:>10.3f}  {d['guess']}")


if __name__ == "__main__":
    main()
