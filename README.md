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

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:**

**The numbers:**

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**



---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human |  |  |
| unsure |  |  |
| high-confidence AI |  |  |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->



---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "...", "creator_id": "..."}'
```

```json

```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "...", "reasoning": "..."}'
```

```json

```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json

```

---

## How I Used AI

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

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
