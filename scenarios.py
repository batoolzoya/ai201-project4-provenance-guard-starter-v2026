"""
What my five criteria are tested with. run_eval.py runs everything here three
times:  python run_eval.py --label before

My own writing is NOT in this file. It is read from private/my_writing.txt and
private/extra.txt, which are git-ignored (pieces separated by a line of ---),
because the repo is public. Reports show "my piece #N", never the text. A
grader can see what was run (which pieces, how many) but not read my writing.

A scenario carries one of:
    "texts"         strings, each sent as {"text": ..., "creator_id": ...}
    "bodies"        whole request bodies, sent exactly as written
    "appeal_texts"  strings that are submitted, then appealed (criterion 4)
Optional:
    "names"         what the report shows instead of the text
    "groups"        {"group name": [indexes]} — the report gives each group's
                    mean combined score per trial (criterion 3)
"""

from pathlib import Path

PRIVATE = Path(__file__).parent / "private"


def _pieces(filename):
    path = PRIVATE / filename
    if not path.exists():
        return []
    raw = path.read_text(encoding="utf-8-sig")
    return [p.strip() for p in raw.split("\n---") if p.strip().strip("-").strip()]


def _first_sentences(text, n=2):
    import stylometry
    return " ".join(stylometry.sentences(text)[:n])


MY_WRITING = _pieces("my_writing.txt")
MY_EXTRA = _pieces("extra.txt")

# ── AI-generated text (written by Claude for these tests) ─────────────────────

# Clearly AI. AI_CLEAR_1 is the calibration text from unit 7.
AI_CLEAR = [
    "Time management is an essential skill for students who want to succeed "
    "academically. By creating a schedule and prioritizing tasks, students can "
    "reduce stress and improve their overall performance. Additionally, it is "
    "important to take regular breaks to maintain focus and productivity. "
    "Ultimately, developing good time management habits can lead to long-term "
    "success in both school and life.",

    "Regular physical activity offers numerous benefits for both physical and "
    "mental health. Engaging in exercise can help individuals maintain a healthy "
    "weight, reduce the risk of chronic diseases, and improve cardiovascular "
    "fitness. Furthermore, exercise has been shown to reduce symptoms of anxiety "
    "and depression. Overall, incorporating physical activity into daily life is "
    "an important step toward a healthier lifestyle.",

    "Technology has transformed the way people communicate in the modern world. "
    "Social media platforms, messaging applications, and video calls allow "
    "individuals to stay connected regardless of distance. However, it is "
    "important to consider the potential drawbacks, such as reduced face-to-face "
    "interaction. In conclusion, technology provides valuable tools for "
    "communication when used thoughtfully and responsibly.",
]

# AI paragraphs that get two of my own sentences put in front of them, to make
# the borderline inputs (mixed authorship).
AI_FOR_MIXING = [
    "Effective study habits are crucial for academic success. Students who "
    "review material consistently tend to retain information more effectively. "
    "Additionally, creating a dedicated study environment can minimize "
    "distractions and enhance concentration.",

    "Reading for pleasure provides a wide range of cognitive and emotional "
    "benefits. It can expand vocabulary, improve focus, and offer a valuable "
    "escape from daily stress. Furthermore, reading regularly has been linked to "
    "greater empathy and understanding of others.",

    "Volunteering in the community is a meaningful way to make a positive "
    "impact. It allows individuals to develop new skills, build connections, and "
    "contribute to causes they care about. Ultimately, volunteering benefits both "
    "the volunteer and the community as a whole.",
]

BORDERLINE = [
    _first_sentences(mine) + " " + ai
    for mine, ai in zip(MY_EXTRA, AI_FOR_MIXING)
]

# My pieces #8, #9 and #10 (1-based), chosen knowing that in unit 7 #10 was the
# only one of my pieces to reach the "human" label.
MY_THREE = MY_WRITING[7:10]


SCENARIOS = [
    {
        "name": "my own writing",
        "criterion": 1,
        "texts": MY_WRITING,
        "names": [f"my piece #{i}" for i in range(1, len(MY_WRITING) + 1)],
    },
    {
        "name": "label coverage",
        "criterion": 2,
        "texts": AI_CLEAR + MY_THREE + BORDERLINE,
        "names": (["clearly AI #1", "clearly AI #2", "clearly AI #3"]
                  + ["my piece #8", "my piece #9", "my piece #10"]
                  + ["borderline #1 (my 2 sentences + AI)",
                     "borderline #2 (my 2 sentences + AI)",
                     "borderline #3 (my 2 sentences + AI)"]),
    },
    {
        "name": "score spread",
        "criterion": 3,
        "texts": AI_CLEAR + MY_THREE,
        "names": ["clearly AI #1", "clearly AI #2", "clearly AI #3",
                  "my piece #8", "my piece #9", "my piece #10"],
        "groups": {"clearly AI": [0, 1, 2], "my pieces": [3, 4, 5]},
    },
    {
        "name": "appeal path",
        "criterion": 4,
        # Five submissions, each then appealed; plus one appeal with a
        # made-up content_id, which should come back 404.
        "appeal_texts": AI_CLEAR + AI_FOR_MIXING[:2],
    },
    {
        "name": "bad input",
        "criterion": 5,
        "bodies": [
            {"text": "", "creator_id": "eval_bad_empty"},
            {"creator_id": "eval_bad_missing"},
            {"text": None, "creator_id": "eval_bad_null"},
            {"text": 12345, "creator_id": "eval_bad_number"},
            {"text": "word " * 5000, "creator_id": "eval_bad_huge"},  # 25,000 chars
            {"text": "A short piece of writing with no creator at all."},
        ],
        "names": ["empty text", "no text field", "text null", "text is a number",
                  "text over 20,000 characters", "no creator_id"],
    },
]


def validate() -> list[str]:
    """Complain about anything malformed, before a long run rather than during."""
    problems = []
    if len(MY_WRITING) != 10:
        problems.append(f"expected 10 pieces in private/my_writing.txt, found "
                        f"{len(MY_WRITING)} — is the private/ folder there?")
    if len(MY_EXTRA) < 3:
        problems.append(f"expected 3 pieces in private/extra.txt, found {len(MY_EXTRA)}")
    for i, scenario in enumerate(SCENARIOS, 1):
        kinds = [k for k in ("texts", "bodies", "appeal_texts") if scenario.get(k)]
        if len(kinds) != 1:
            problems.append(f"scenario {i} ('{scenario.get('name')}') needs exactly "
                            f"one of texts / bodies / appeal_texts")
            continue
        items = scenario[kinds[0]]
        names = scenario.get("names")
        if names and len(names) != len(items):
            problems.append(f"scenario {i}: {len(names)} names for {len(items)} items")
        if kinds[0] == "bodies":
            if not all(isinstance(b, dict) for b in items):
                problems.append(f"scenario {i}: every body must be a dict")
        elif not all(isinstance(t, str) and t.strip() for t in items):
            problems.append(f"scenario {i}: an empty text — use 'bodies' for that")
    return problems
