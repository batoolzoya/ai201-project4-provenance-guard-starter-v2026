# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-19 22:19
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `14d68787-cace-4fa8-9c63-9547b0e56343` | unsure | 0.360 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `981d1757-b11c-4bbc-ae42-e7d201df1bc9` | unsure | 0.371 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `2ec14959-a2d4-4978-97e0-37319d8f7ad2` | unsure | 0.461 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `8e924d88-9710-4271-bd35-8c8249b22923` | unsure | 0.537 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `43175e7e-f4d3-44ba-a5af-e9e772d568b7` | human | 0.200 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `ddf79e64-ca87-4333-9ce6-3b5a50f325b5` | unsure | 0.404 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `e2975b6d-c09e-4c78-9d56-9c9df18ed089` | unsure | 0.374 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `af2347b8-66e8-40cd-bee7-e19fc93a32a2` | unsure | 0.360 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `6f451554-0f42-41f6-8f52-2bff0d28e0bb` | unsure | 0.530 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `35687218-767f-4c1a-9521-9ac0bf2045ad` | ai | 0.903 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `37298961-cf02-4ba6-8f1e-c4d9453fea96` | unsure | 0.514 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `62b4b7ea-3a03-4c13-abbd-91606e0470d4` | unsure | 0.682 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `d46e8267-5405-48e6-b2ca-1d436b26ec3c` | unsure | 0.678 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `2ecfbcfa-dca5-43c8-9596-a61e29fd9d5d` | unsure | 0.686 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `8bd14c00-68f8-4ee8-b12f-2ffe8ddfb128` | ai | 0.784 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `5ac09181-9bf9-411e-a499-7c03e1e00a0a` | ai | 0.707 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `f08eb852-a607-493b-bd7d-6eefaf181f0b` | ai | 0.740 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `51e197f1-6e8c-4110-b760-8ccce4d50482` | human | 0.334 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `222b6a08-05f9-4289-8e1e-a6dabdb96b20` | human | 0.339 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `2e5e1da9-5a34-4e4b-888b-e681a5ac9eb6` | human | 0.183 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `c8b254c9-79c4-43fa-be8c-88aca8f4b7ca` | unsure | 0.403 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `1a1dfdc4-37db-4026-a803-f120aa0e175d` | unsure | 0.366 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `a748596a-448c-4d89-8e09-fadf52e30946` | unsure | 0.383 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `1df807f6-8863-4c84-b295-037a8a7d7bdd` | unsure | 0.478 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 400 | `—` | — | — |  |
| MF04 | malformed | text is only punctuation | 400 | `—` | — | — |  |
| MF05 | malformed | text is a very long single word | 400 | `—` | — | — |  |
| MF06 | malformed | text is emoji only | 400 | `—` | — | — |  |
| MF07 | malformed | text is right-to-left script | 200 | `d1508fe1-eb77-4537-8a93-5b96a39c2f38` | unsure | — |  |
| MF08 | malformed | text is 60,000 characters | 400 | `—` | — | — |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `b6840bfb-0452-4334-aea3-5429a0f714ed` | unsure | 0.360 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `2de1d3d4-99cb-4735-93c1-1c6a5e1e9002` | unsure | 0.360 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `5f62d98e-17c2-49e8-b0c0-a615ea9709b6` | unsure | 0.360 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `e946d616-c9e4-449e-8413-305776b16200` | unsure | 0.360 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c3296c46-7a4d-4677-90fe-11b91851f86e` | unsure | 0.360 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "14d68787-cace-4fa8-9c63-9547b0e56343",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.36,
  "model_score": 0.1156,
  "style_score": 0.6379,
  "label": "Our automated check couldn't tell whether this was written by a person or with an AI tool. That happens often with ordinary writing, and it is not an accusation. If you'd like a person to look at it, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "981d1757-b11c-4bbc-ae42-e7d201df1bc9",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.3708,
  "model_score": 0.4949,
  "style_score": 0.1846,
  "label": "Our automated check couldn't tell whether this was written by a person or with an AI tool. That happens often with ordinary writing, and it is not an accusation. If you'd like a person to look at it, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "2ec14959-a2d4-4978-97e0-37319d8f7ad2",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.461,
  "model_score": 0.5718,
  "style_score": 0.2949,
  "label": "Our automated check couldn't tell whether this was written by a person or with an AI tool. That happens often with ordinary writing, and it is not an accusation. If you'd like a person to look at it, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "8e924d88-9710-4271-bd35-8c8249b22923",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.5372,
  "model_score": 0.5128,
  "style_score": 0.5737,
  "label": "Our automated check couldn't tell whether this was written by a person or with an AI tool. That happens often with ordinary writing, and it is not an accusation. If you'd like a person to look at it, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "43175e7e-f4d3-44ba-a5af-e9e772d568b7",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.2,
  "model_score": 0.2404,
  "style_score": 0.1393,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "ddf79e64-ca87-4333-9ce6-3b5a50f325b5",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.4042,
  "model_score": 0.4727,
  "style_score": 0.3014,
  "label": "Our automated check couldn't tell whether this was written by a person or with an AI tool. That happens often with ordinary writing, and it is not an accusation. If you'd like a person to look at it, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "e2975b6d-c09e-4c78-9d56-9c9df18ed089",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.3741,
  "model_score": 0.4865,
  "style_score": 0.2055,
  "label": "Our automated check couldn't tell whether this was written by a person or with an AI tool. That happens often with ordinary writing, and it is not an accusation. If you'd like a person to look at it, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "af2347b8-66e8-40cd-bee7-e19fc93a32a2",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.36,
  "model_score": 0.1785,
  "style_score": 0.5938,
  "label": "Our automated check couldn't tell whether this was written by a person or with an AI tool. That happens often with ordinary writing, and it is not an accusation. If you'd like a person to look at it, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "6f451554-0f42-41f6-8f52-2bff0d28e0bb",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.5303,
  "model_score": 0.6143,
  "style_score": 0.4043,
  "label": "Our automated check couldn't tell whether this was written by a person or with an AI tool. That happens often with ordinary writing, and it is not an accusation. If you'd like a person to look at it, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "35687218-767f-4c1a-9521-9ac0bf2045ad",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.9035,
  "model_score": 0.9692,
  "style_score": 0.8049,
  "label": "This piece reads very much like text written by an AI tool. This is an automated guess, not proof, and it can be wrong. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "37298961-cf02-4ba6-8f1e-c4d9453fea96",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.5141,
  "model_score": 0.5192,
  "style_score": 0.5064,
  "label": "Our automated check couldn't tell whether this was written by a person or with an AI tool. That happens often with ordinary writing, and it is not an accusation. If you'd like a person to look at it, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "62b4b7ea-3a03-4c13-abbd-91606e0470d4",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.6821,
  "model_score": 0.6541,
  "style_score": 0.7242,
  "label": "Our automated check couldn't tell whether this was written by a person or with an AI tool. That happens often with ordinary writing, and it is not an accusation. If you'd like a person to look at it, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "d46e8267-5405-48e6-b2ca-1d436b26ec3c",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.6783,
  "model_score": 0.7343,
  "style_score": 0.5942,
  "label": "Our automated check couldn't tell whether this was written by a person or with an AI tool. That happens often with ordinary writing, and it is not an accusation. If you'd like a person to look at it, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "2ecfbcfa-dca5-43c8-9596-a61e29fd9d5d",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.6861,
  "model_score": 0.7693,
  "style_score": 0.5613,
  "label": "Our automated check couldn't tell whether this was written by a person or with an AI tool. That happens often with ordinary writing, and it is not an accusation. If you'd like a person to look at it, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "8bd14c00-68f8-4ee8-b12f-2ffe8ddfb128",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.7842,
  "model_score": 0.7286,
  "style_score": 0.8676,
  "label": "This piece reads very much like text written by an AI tool. This is an automated guess, not proof, and it can be wrong. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "5ac09181-9bf9-411e-a499-7c03e1e00a0a",
  "creator_id": "attacker_FP06",
  "guess": "ai",
  "confidence": 0.7065,
  "model_score": 0.8326,
  "style_score": 0.5174,
  "label": "This piece reads very much like text written by an AI tool. This is an automated guess, not proof, and it can be wrong. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "f08eb852-a607-493b-bd7d-6eefaf181f0b",
  "creator_id": "attacker_FP07",
  "guess": "ai",
  "confidence": 0.7397,
  "model_score": 0.8328,
  "style_score": 0.6,
  "label": "This piece reads very much like text written by an AI tool. This is an automated guess, not proof, and it can be wrong. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "51e197f1-6e8c-4110-b760-8ccce4d50482",
  "creator_id": "attacker_FP08",
  "guess": "human",
  "confidence": 0.3343,
  "model_score": 0.2414,
  "style_score": 0.4736,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "222b6a08-05f9-4289-8e1e-a6dabdb96b20",
  "creator_id": "attacker_PI01",
  "guess": "human",
  "confidence": 0.3392,
  "model_score": 0.3653,
  "style_score": 0.3,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "2e5e1da9-5a34-4e4b-888b-e681a5ac9eb6",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.183,
  "model_score": 0.1467,
  "style_score": 0.2375,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "c8b254c9-79c4-43fa-be8c-88aca8f4b7ca",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.4027,
  "model_score": 0.4949,
  "style_score": 0.2643,
  "label": "Our automated check couldn't tell whether this was written by a person or with an AI tool. That happens often with ordinary writing, and it is not an accusation. If you'd like a person to look at it, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "1a1dfdc4-37db-4026-a803-f120aa0e175d",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.3664,
  "model_score": 0.4006,
  "style_score": 0.3151,
  "label": "Our automated check couldn't tell whether this was written by a person or with an AI tool. That happens often with ordinary writing, and it is not an accusation. If you'd like a person to look at it, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "a748596a-448c-4d89-8e09-fadf52e30946",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.3832,
  "model_score": 0.5434,
  "style_score": 0.1429,
  "label": "Our automated check couldn't tell whether this was written by a person or with an AI tool. That happens often with ordinary writing, and it is not an accusation. If you'd like a person to look at it, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "1df807f6-8863-4c84-b295-037a8a7d7bdd",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.4783,
  "model_score": 0.4581,
  "style_score": 0.5087,
  "label": "Our automated check couldn't tell whether this was written by a person or with an AI tool. That happens often with ordinary writing, and it is not an accusation. If you'd like a person to look at it, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF06",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "d1508fe1-eb77-4537-8a93-5b96a39c2f38",
  "creator_id": "attacker_MF07",
  "guess": "unsure",
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": "Our automated check couldn't tell whether this was written by a person or with an AI tool. That happens often with ordinary writing, and it is not an accusation. If you'd like a person to look at it, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "b6840bfb-0452-4334-aea3-5429a0f714ed",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.36,
  "model_score": 0.0193,
  "style_score": 0.5,
  "label": "Our automated check couldn't tell whether this was written by a person or with an AI tool. That happens often with ordinary writing, and it is not an accusation. If you'd like a person to look at it, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "2de1d3d4-99cb-4735-93c1-1c6a5e1e9002",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.36,
  "model_score": 0.0193,
  "style_score": 0.5,
  "label": "Our automated check couldn't tell whether this was written by a person or with an AI tool. That happens often with ordinary writing, and it is not an accusation. If you'd like a person to look at it, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "5f62d98e-17c2-49e8-b0c0-a615ea9709b6",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.36,
  "model_score": 0.0193,
  "style_score": 0.5,
  "label": "Our automated check couldn't tell whether this was written by a person or with an AI tool. That happens often with ordinary writing, and it is not an accusation. If you'd like a person to look at it, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "e946d616-c9e4-449e-8413-305776b16200",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.36,
  "model_score": 0.0193,
  "style_score": 0.5,
  "label": "Our automated check couldn't tell whether this was written by a person or with an AI tool. That happens often with ordinary writing, and it is not an accusation. If you'd like a person to look at it, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "c3296c46-7a4d-4677-90fe-11b91851f86e",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.36,
  "model_score": 0.0193,
  "style_score": 0.5,
  "label": "Our automated check couldn't tell whether this was written by a person or with an AI tool. That happens often with ordinary writing, and it is not an accusation. If you'd like a person to look at it, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
