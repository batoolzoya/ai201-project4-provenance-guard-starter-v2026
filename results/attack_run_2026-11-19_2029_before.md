# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-19 20:29
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
| EV01 | evasion | signal two: typos raise word variety | 200 | `a2e1d4ac-5394-4b9a-ad35-07f84b88a0f8` | unsure | 0.360 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `c0748365-48a2-466d-9661-1b0f5b1e005c` | unsure | 0.371 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `8c3d2aa3-8018-4607-8fd6-278a09d55b55` | unsure | 0.461 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `218959c1-f315-4bd3-bc63-77aebe35551e` | unsure | 0.537 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `9b8ce64c-3caa-4584-8deb-62eb57f98438` | human | 0.200 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `318dc4ff-2a08-416e-8a5b-ef89a74b3cbf` | unsure | 0.404 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `1e239182-be50-457e-9799-3408d0d3c65d` | unsure | 0.374 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `f0f571d6-a8d9-4ca6-90ec-d45d233fa5d9` | unsure | 0.360 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `8832c5ac-059b-47f6-a5b3-6237cfb71ce5` | unsure | 0.530 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `d2ddc56d-97a6-4187-94be-8bfb073920f5` | ai | 0.903 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `b8f2a9e5-773c-4c09-ae19-e7c1bc18ebbd` | unsure | 0.514 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `c5374088-5f58-4c53-8b33-67d447ce0935` | unsure | 0.682 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `daff6071-6eac-443e-918f-1c4aebb0ea3e` | unsure | 0.678 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `9422b006-ae3b-48e8-b8c5-1c1ab0a4798a` | unsure | 0.686 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `693e3d0f-04a4-4b2a-9286-a968399d3dc9` | ai | 0.784 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `1ea35411-b7f7-4892-8eed-d6cc1c4cd708` | ai | 0.707 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `628c3144-8308-4459-bce9-c69d19e92343` | ai | 0.740 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `43760db1-d52f-408d-a9e7-611eb5722ef4` | human | 0.334 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `7ddfa21a-112b-4749-bdbb-550428dae192` | human | 0.339 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `3f3133df-b05e-40ea-b0c2-cb30d1900f2a` | human | 0.183 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `2528bc52-c7fb-4515-b057-ce8ce951c807` | unsure | 0.403 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `92a4e218-3aa0-4b77-bf37-6ae352d1b0a4` | unsure | 0.366 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `caec7898-14f1-45a9-aa22-c4c5d3663375` | unsure | 0.383 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `19f86cad-015f-4bec-a3ce-96dec45048c0` | unsure | 0.478 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 400 | `—` | — | — |  |
| MF04 | malformed | text is only punctuation | 200 | `990ad47a-4065-4a3e-bf93-b2c1d46bda6c` | unsure | 0.360 |  |
| MF05 | malformed | text is a very long single word | 400 | `—` | — | — |  |
| MF06 | malformed | text is emoji only | 400 | `—` | — | — |  |
| MF07 | malformed | text is right-to-left script | 200 | `34cfda11-c393-4551-85ca-811e12482f18` | ai | 0.840 |  |
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
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `452ebee1-5ccc-426e-9b68-145edc71ecbb` | unsure | 0.360 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `061a15b1-8002-44d8-98a4-dbd42b0b6f63` | unsure | 0.360 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `e31d8577-b415-4ea0-8188-c11736136436` | unsure | 0.360 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `5f495f9b-d4c4-44e9-bdfe-41b5d80a0f6a` | unsure | 0.360 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `4e80c6dd-f319-4f00-9b5e-3e8f1b9b3b77` | unsure | 0.360 |  |
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
  "content_id": "a2e1d4ac-5394-4b9a-ad35-07f84b88a0f8",
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
  "content_id": "c0748365-48a2-466d-9661-1b0f5b1e005c",
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
  "content_id": "8c3d2aa3-8018-4607-8fd6-278a09d55b55",
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
  "content_id": "218959c1-f315-4bd3-bc63-77aebe35551e",
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
  "content_id": "9b8ce64c-3caa-4584-8deb-62eb57f98438",
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
  "content_id": "318dc4ff-2a08-416e-8a5b-ef89a74b3cbf",
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
  "content_id": "1e239182-be50-457e-9799-3408d0d3c65d",
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
  "content_id": "f0f571d6-a8d9-4ca6-90ec-d45d233fa5d9",
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
  "content_id": "8832c5ac-059b-47f6-a5b3-6237cfb71ce5",
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
  "content_id": "d2ddc56d-97a6-4187-94be-8bfb073920f5",
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
  "content_id": "b8f2a9e5-773c-4c09-ae19-e7c1bc18ebbd",
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
  "content_id": "c5374088-5f58-4c53-8b33-67d447ce0935",
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
  "content_id": "daff6071-6eac-443e-918f-1c4aebb0ea3e",
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
  "content_id": "9422b006-ae3b-48e8-b8c5-1c1ab0a4798a",
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
  "content_id": "693e3d0f-04a4-4b2a-9286-a968399d3dc9",
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
  "content_id": "1ea35411-b7f7-4892-8eed-d6cc1c4cd708",
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
  "content_id": "628c3144-8308-4459-bce9-c69d19e92343",
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
  "content_id": "43760db1-d52f-408d-a9e7-611eb5722ef4",
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
  "content_id": "7ddfa21a-112b-4749-bdbb-550428dae192",
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
  "content_id": "3f3133df-b05e-40ea-b0c2-cb30d1900f2a",
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
  "content_id": "2528bc52-c7fb-4515-b057-ce8ce951c807",
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
  "content_id": "92a4e218-3aa0-4b77-bf37-6ae352d1b0a4",
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
  "content_id": "caec7898-14f1-45a9-aa22-c4c5d3663375",
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
  "content_id": "19f86cad-015f-4bec-a3ce-96dec45048c0",
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
  "status": 200,
  "content_id": "990ad47a-4065-4a3e-bf93-b2c1d46bda6c",
  "creator_id": "attacker_MF04",
  "guess": "unsure",
  "confidence": 0.36,
  "model_score": 0.0075,
  "style_score": 0.5,
  "label": "Our automated check couldn't tell whether this was written by a person or with an AI tool. That happens often with ordinary writing, and it is not an accusation. If you'd like a person to look at it, you can ask for a review.",
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
  "content_id": "34cfda11-c393-4551-85ca-811e12482f18",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.8398,
  "model_score": 0.8663,
  "style_score": 0.8,
  "label": "This piece reads very much like text written by an AI tool. This is an automated guess, not proof, and it can be wrong. If you wrote it yourself, you can appeal and a person will review it.",
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
  "content_id": "452ebee1-5ccc-426e-9b68-145edc71ecbb",
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
  "content_id": "061a15b1-8002-44d8-98a4-dbd42b0b6f63",
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
  "content_id": "e31d8577-b415-4ea0-8188-c11736136436",
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
  "content_id": "5f495f9b-d4c4-44e9-bdfe-41b5d80a0f6a",
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
  "content_id": "4e80c6dd-f319-4f00-9b5e-3e8f1b9b3b77",
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
