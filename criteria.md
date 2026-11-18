# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. My own writing is rarely called AI (false positives)

Of my 10 pieces of my own writing, at most 1 get the high-confidence AI label,
in every one of three trials.

**Why this target:**

None of the excerpts are just a couple sentences. They are long enough that each provides sufficient data for the model to conclude it not to be AI-written predictable writing, with sufficient margin for error.

---

## 2. All three labels are reachable (label coverage)

My 9 coverage inputs (3 AI-generated, 3 of my own pieces, 3 I judge borderline)
produce all 3 labels (human, unsure, AI) at least once, in every one of three
trials.

**Why this target:**

It is reasonable to expect an effective system to be capable of identifying each category at least once in every one of three trials. 

---

## 3. AI text and my text score clearly apart (score spread)

The average combined score of 3 clearly AI-generated texts is at least 0.5
higher than the average combined score of 3 of my own pieces, in every one of
three trials.

**Why this target:**

We want the system to be confident enough that there is at least an average .5 point spread between the clear AI and human generated cases.

---

## 4. Appeals always change status and are always recorded (appeal path)

In every one of the three trials, 5 of 5 appeals sent with a real content_id return 200 and the audit log then shows status under_review for that id. An appeal with a made-up content_id returns 404, not 200.

**Why this target:**

The writers should be able to rely upon their appeals being considered.

---

## 5. Bad input is refused cleanly (bad input)

All 6 malformed requests (empty text, no text field, text null, a number instead
of text, text over 20,000 characters, no creator_id) return 400, none return 500,
and each one leaves a rejected entry in the audit log, in every one of three
trials.

**Why this target:**

We should be able to maintain a log trace every time.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
