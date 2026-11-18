# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

Provenance Guard is a small web service a writing site could plug into. A piece
of writing goes in; a guess, a confidence score, a plain-English label and an
appeal route come out.

**The path a submission takes**

1. **The site sends it in.** `POST /submit` with JSON `{"text": ..., "creator_id": ...}`.
2. **The route checks it** (`app.py::submit`). Text must be a string with at
   least 5 words and at most 20,000 characters, and `creator_id` must be present.
   Anything else gets a `400` with a reason, and the refusal is written to the
   audit log so it isn't invisible.
3. **It gets an id.** A new `content_id` (a UUID) is created. The appeal needs it later.
4. **Signal one reads it** (`detector.py::model_signal`). GPT-2, running locally,
   measures how predictable the text is → a 0–1 score (higher = more AI-like).
5. **Signal two measures it** (`stylometry.py::style_signal`). Sentence-length
   spread, vocabulary variety and punctuation variety → a 0–1 score (higher = more AI-like).
6. **The two become one number** (`scoring.py::combine_signals`) — the confidence score.
7. **The number becomes words** (`scoring.py::score_to_label`). The score falls in
   one of three bands, and each band has a full sentence a writer reads.
8. **It is logged and answered.** `audit.log_decision` writes timestamp, ids, both
   signal scores, the combined score, the guess, the label and `status: decided`
   to `logs/audit.jsonl`, and the same fields go back to the caller as JSON.
9. **The writer can push back.** `POST /appeal` with the `content_id` and their
   reasoning records the appeal next to the original decision and moves the item
   to `under_review`. Nothing is re-scored automatically; a person looks at it.

**Following a false positive through the service**

A writer posts a short paragraph they wrote themselves, in plain, simple
sentences with everyday words. GPT-2 finds plain writing easy to predict, so
signal one scores it high (around 0.8, the same range as real AI text). If their
sentences are also evenly sized, signal two agrees, and the combined score lands
in the high-confidence AI band. The label they see says the system thinks a
computer probably wrote their work. What they can do: send an appeal with their
reasoning, which puts the item under review and records their side next to the
decision. Nothing else protects them, so this is the case my thresholds are set
around: the AI band should start high enough that one signal on its own can't
put someone there.

**The two endpoints (the contract)**

`POST /submit`

| Direction | Field | Type | Notes |
|---|---|---|---|
| in | `text` | string | required; 5+ words; max 20,000 characters |
| in | `creator_id` | string | required; who wrote it |
| out (200) | `content_id` | string | UUID; use it to appeal |
| out (200) | `guess` | string | `"ai"`, `"human"` or `"unsure"` |
| out (200) | `confidence` | number | combined score, 0.0 (human) – 1.0 (AI) |
| out (200) | `label` | string | the sentence a reader sees |
| out (200) | `model_score` | number | signal one, 0–1 |
| out (200) | `style_score` | number | signal two, 0–1 |
| out (200) | `status` | string | `"decided"` |
| out (400) | `error`, `message` | string | e.g. `"missing_text"`, `"text_too_short"`, `"text_too_long"` |

`POST /appeal`

| Direction | Field | Type | Notes |
|---|---|---|---|
| in | `content_id` | string | required; must be one `/submit` returned |
| in | `reasoning` | string | required; the writer's explanation |
| out (200) | `content_id` | string | echoed back |
| out (200) | `status` | string | `"under_review"` |
| out (200) | `message` | string | confirmation for the writer |
| out (400) | `error`, `message` | string | missing `content_id` or `reasoning` |
| out (404) | `error`, `message` | string | `content_id` not found |

---

## Signals and Scoring

### Signal one — the model signal

**What it measures:** How predictable the text is to GPT-2 (perplexity), squashed
to 0–1 so that low perplexity = high score = more AI-like.

**Why that might differ between human and AI writing:** A language model writes
by picking likely next words, so its output is text a model finds easy to
predict. People make odder, more specific word choices.

**What it can't see:** Who actually wrote it. It rewards common words in short,
ordinary sentences, so plain human writing (second-language writers, younger
writers, anyone writing simply on purpose) scores as AI. And the reverse: AI text
with rare or ornate words swapped in scores as human.

### Signal two — the style signal

**What it measures:** The shape of the text, without reading it: how much
sentence lengths vary, how varied the vocabulary is, and how varied the
punctuation is (commas, semicolons, dashes, brackets, question marks).

**Why that might differ between human and AI writing:** Generated prose tends
toward even, mid-length sentences and safe, tidy punctuation. Human writing is
lumpier: a three-word sentence next to a long one, a dash, a fragment.

**What it can't see:** Meaning. Anything that changes the shape without changing
the substance moves it: adding typos, splitting or joining sentences, adding
dashes, pasting in a quote. That's cheap to do on purpose. It also can't tell a
careful human writer with very even sentences from a model.

### The combining rule

**The rule:** A weighted average of the two signals, plus one rule for when they
disagree. If the two signals are more than 0.4 apart, the combined score is held
inside the unsure band (0.36 – 0.69), whatever the average says. Two different
methods disagreeing that strongly *is* uncertainty, and I don't want one signal
on its own to be able to put a writer's work in the AI band.

**The numbers** (all in `config.py`):

| Setting | Value | Why |
|---|---|---|
| `WEIGHT_MODEL_SIGNAL` | 0.6 | it reads the whole text, not just surface features |
| `WEIGHT_STYLE_SIGNAL` | 0.4 | cheap to fool (typos, split sentences), so it counts less |
| `DISAGREEMENT_GAP` | 0.4 | a gap bigger than this means "unsure" |
| `HUMAN_THRESHOLD` | 0.35 | at or below → high-confidence human |
| `AI_THRESHOLD` | 0.70 | at or above → high-confidence AI. Set so a model score of 1.0 with a style score of 0 only reaches 0.60: both signals have to lean AI |

Inside signal two (`stylometry.py::style_signal`): each measure is mapped onto
0–1 "AI-likeness" between two anchor values, then
`style = 0.4 × sentence-length spread + 0.3 × vocabulary variety (MATTR) + 0.3 × expressive punctuation`.

**Where it lives:** `scoring.py::combine_signals`

**One calibration change, made in Milestone 5:** signal one maps perplexity to
0–1 around a midpoint, the perplexity that scores 0.5. The starter's midpoint
was 45. With it, my own writing (perplexity about 23–40) scored 0.55–0.74 on
signal one, and none of 13 human pieces could reach the human label: the lowest
combined score was 0.371. I moved the midpoint to **35** in
`detector.py::model_signal`. The clearly-AI text still scores 0.84 on signal one.
The cost is that every model score drops, so AI text slips through more easily.
I tuned this on my own writing, which is also the test set for criterion 1, so
that criterion got a little easier to meet.

**Calibration inputs** (real runs of `try_inputs.py`; my own pieces are kept out
of the repo, so only scores are shown)

| Input | Model (mid 45) | Style | Combined (mid 45) | Model (mid 35) | Combined (mid 35) | Label (mid 35) |
|---|---|---|---|---|---|---|
| clearly AI | 0.885 | 0.606 | 0.774 | 0.838 | 0.745 | AI |
| lightly-edited AI | 0.456 | 0.390 | 0.429 | 0.359 | 0.371 | unsure |
| my piece #1 | 0.616 | 0.405 | 0.531 | 0.518 | 0.472 | unsure |
| my piece #2 | 0.718 | 0.442 | 0.607 | 0.630 | 0.554 | unsure |
| my piece #3 | 0.722 | 0.349 | 0.572 | 0.634 | 0.520 | unsure |
| my piece #4 | 0.690 | 0.501 | 0.614 | 0.598 | 0.559 | unsure |
| my piece #5 | 0.551 | 0.536 | 0.545 | 0.451 | 0.485 | unsure |
| my piece #6 | 0.716 | 0.185 | 0.504 | 0.628 | 0.451 | unsure |
| my piece #7 | 0.740 | 0.385 | 0.598 | 0.655 | 0.547 | unsure |
| my piece #8 | 0.636 | 0.256 | 0.484 | 0.539 | 0.426 | unsure |
| my piece #9 | 0.624 | 0.585 | 0.608 | 0.526 | 0.550 | unsure |
| my piece #10 | 0.362 | 0.385 | 0.371 | 0.275 | 0.319 | **human** |
| my extra #1 | 0.622 | 0.113 | 0.418 | 0.524 | 0.360 | unsure |
| my extra #2 | 0.605 | 0.327 | 0.494 | 0.506 | 0.435 | unsure |
| my extra #3 | 0.460 | 0.801 | 0.597 | 0.363 | 0.538 | unsure |

What this shows: signal one leans AI on almost all of my writing, and signal two
is what pulls it back. Light editing (contractions, a dash, a split sentence)
dropped the AI text from 0.885 to 0.456 on signal one, which is a weak spot to
expect in the next unit's attacks.

**A case where my two signals split, and what my rule does with it:**

My piece #6: signal one 0.628 ("leans AI"), signal two 0.185 ("very human"), a
gap of 0.44. That is over 0.4, so the disagreement rule applies and the result
is held in the unsure band: combined 0.451, unsure. Here the plain average
(0.451) was already in the band, so the rule changed nothing. It matters when one
signal is extreme: model 1.0 with style 0.5 averages to 0.80 (AI), but the gap
is 0.5, so the rule holds it at 0.69 (unsure). My extra #1 (0.524 vs 0.113, gap
0.41) is the closest real case: the average 0.359 was raised to 0.36. Both are
unsure, so the label didn't change.

---

## Label Variants

Score ranges come from `scoring.label_ranges()`. Every score from 0 to 1 falls
in exactly one band, and all three were reached by real submissions (table above).

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.35 | We think this was written by a person. |
| unsure | above 0.35, below 0.70 | Our automated check couldn't tell whether this was written by a person or with an AI tool. That happens often with ordinary writing, and it is not an accusation. If you'd like a person to look at it, you can ask for a review. |
| high-confidence AI | 0.70 – 1.00 | This piece reads very much like text written by an AI tool. This is an automated guess, not proof, and it can be wrong. If you wrote it yourself, you can appeal and a person will review it. |

**Why I worded the "unsure" one this way:**

All 10 of my own pieces got this label, so it's the one real writers will see
most. It has to admit the system doesn't know, say that this happens to ordinary
writing, and say plainly that it isn't an accusation, while still giving the
writer a next step. When I had the labels read back as a writer would, the risk
was that "not an accusation" could still make someone feel suspected, and that
"review of what?" isn't obvious. I kept the wording and noted it as something
the next unit could test.

---

## Sample Run

**A submission** (after the Milestone 5 recalibration)

```bash
$ curl.exe -X POST http://127.0.0.1:5000/submit -H "Content-Type: application/json" -d '{\"text\": \"Time management is an essential skill for students who want to succeed academically. By creating a schedule and prioritizing tasks, students can reduce stress and improve their overall performance.\", \"creator_id\": \"zoya\"}'
```

```json
{
  "confidence": 0.7787,
  "content_id": "436bb0c7-58ac-4243-a2b1-4867101b452c",
  "guess": "ai",
  "label": "This piece reads very much like text written by an AI tool. This is an automated guess, not proof, and it can be wrong. If you wrote it yourself, you can appeal and a person will review it.",
  "model_score": 0.8311,
  "status": "decided",
  "style_score": 0.7
}
```

I sent this text twice with identical results. The response above is from the
second send (`436bb0c7-…`); the appeal below used the first one's id
(`343ee138-…`), whose log entry is shown at the end of this section. Same text,
same scores.

**An appeal**

```bash
$ curl.exe -X POST http://127.0.0.1:5000/appeal -H "Content-Type: application/json" -d '{\"content_id\": \"343ee138-7f94-4d63-8162-225029ab5235\", \"reasoning\": \"I wrote this myself for a class discussion post.\"}'
```

```json
{
  "content_id": "343ee138-7f94-4d63-8162-225029ab5235",
  "message": "Thanks — your appeal is recorded and a person will review this decision. The original label stays until then.",
  "status": "under_review"
}
```

**What the log shows afterwards**

```bash
$ curl.exe "http://127.0.0.1:5000/log?limit=2"
```

```json
{
  "count": 2,
  "entries": [
    {
      "content_id": "NEW_ID_HERE",
      "creator_id": "unknown",
      "event": "rejected",
      "http_status": 404,
      "reason": "unknown_content_id",
      "status": "rejected",
      "timestamp": "2026-11-18T06:59:02+00:00"
    },
    {
      "content_id": "343ee138-7f94-4d63-8162-225029ab5235",
      "creator_id": "zoya",
      "event": "appeal",
      "reasoning": "I wrote this myself for a class discussion post.",
      "status": "under_review",
      "timestamp": "2026-11-18T07:00:53+00:00"
    }
  ]
}
```

The first entry is a real mistake of mine: I sent the placeholder `NEW_ID_HERE`
instead of the id. The service refused it with a 404 and logged the refusal,
which is what criterion 4 asks for. The second is the real appeal.

The original decision for that content_id, as it sits in `logs/audit.jsonl`
(the log is append-only, so the appeal sits after it rather than overwriting it):

```json
{
  "combined_score": 0.7787,
  "content_id": "343ee138-7f94-4d63-8162-225029ab5235",
  "creator_id": "zoya",
  "guess": "ai",
  "label": "This piece reads very much like text written by an AI tool. This is an automated guess, not proof, and it can be wrong. If you wrote it yourself, you can appeal and a person will review it.",
  "model_score": 0.8311,
  "status": "decided",
  "style_score": 0.7,
  "text_chars": 197,
  "timestamp": "2026-11-18T06:58:56+00:00"
}
```

---

## How I Used AI

I used Claude to write the code and draft this README from my real output. I
ran everything, wrote the criteria and their numbers, and made the calls below.

**Moment 1**

- *What I asked for:* For criterion 1 (how often my own writing may be called
  AI), I asked Claude to write the message a real writer would send me if they
  were one of the people my rate allows, without telling me if my number was right.
- *What came back:* A message from a writer whose plain-English essay was
  labelled AI, pointing out that my system allows this for "two out of every ten
  writers" and asking whether anyone was going to tell them before they posted.
- *What I changed:* I lowered my target from at most 2 of 10 to at most 1 of 10
  and rewrote the reason.

**Moment 2**

- *What I asked for:* After the first real run, none of my human writing could
  reach the "human" label. I asked what my options were.
- *What came back:* Five options with estimated effects on my real scores: try
  different writing, move signal one's midpoint to 35 or 30, raise the human
  threshold to 0.40, or change nothing and document it. Each came with its cost
  (for example, midpoint 30 would have labelled the lightly-edited AI text "written
  by a person").
- *What I changed:* I chose to move the midpoint from 45 to 35, fixing the
  signal that was miscalibrated rather than moving a threshold. I recorded the
  cost and the fact that I tuned on my own test pieces (see Signals and Scoring).

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
