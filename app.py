#!/usr/bin/env python3
"""
Provenance Guard — the web service.

    python app.py

Then, in another terminal:

    curl -X POST http://127.0.0.1:5000/ping \
      -H "Content-Type: application/json" \
      -d '{"message": "hello"}'

That's the example route. It works right now, before you've written anything.
**Leave it alone** — it's your control. When something breaks later, check that
`/ping` still answers: if it does, the problem is in your handler; if it
doesn't, it's the service itself.

Routes:

    POST /ping        the worked example. Already works. Don't edit it
    POST /submit      text in -> guess, confidence, label (built in M3-M5)
    POST /appeal      a writer contests a decision (built in M5)
    GET  /log         the audit log. Already works
    GET  /health      is the service up, and is the model loaded
"""

import re
import unicodedata
import uuid

from flask import Flask, jsonify, request

import audit
import config

app = Flask(__name__)


# ── Rate limiting — UNIT 8 ────────────────────────────────────────────────────
# Off until you turn it on. In unit 8, Milestone 1:
#
#   1. Set RATE_LIMITING_ENABLED = True in config.py (or AI201_RATE_LIMITS=1)
#   2. Choose your numbers there
#   3. Uncomment the @limiter.limit(...) line on /submit below
#
# The order doesn't matter. While limiting is off, that decorator is a no-op
# that quietly does nothing, so uncommenting it early costs you nothing — but
# it also means no 429 until you've done step 1.
#
# The storage backend is preconfigured, which stops Flask-Limiter printing a
# warning on every start. In-memory is right for one laptop and wrong for
# anything real — a restart forgets every count.

class _LimiterOff:
    """
    Stands in for the real limiter while rate limiting is off.

    It makes @limiter.limit(...) a decorator that returns the route
    untouched, so uncommenting the line before you flip the setting is
    harmless instead of a crash on startup.
    """

    def limit(self, *args, **kwargs):
        return lambda view: view


limiter = _LimiterOff()
if config.RATE_LIMITING_ENABLED:
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address

    def rate_limit_key():
        """
        Who a request counts against.

        Falling back to the caller's address is the easy version. Unit 8's
        stretch asks about per-creator limits instead — and the difference
        matters: one script can look like a thousand callers, and one household
        can look like one.
        """
        payload = request.get_json(silent=True)
        # A body that parses as JSON but isn't an object — a bare list or
        # string — has no .get. Without this guard the key function raises
        # BEFORE the route runs, and a malformed request becomes a 500 that
        # looks like your handler crashed when your handler never ran.
        if not isinstance(payload, dict):
            return get_remote_address()
        creator = payload.get("creator_id")
        return creator if isinstance(creator, str) and creator.strip() else get_remote_address()

    limiter = Limiter(
        key_func=rate_limit_key,
        app=app,
        storage_uri=config.RATE_LIMIT_STORAGE,
        default_limits=[],
    )

    @app.errorhandler(429)
    def rate_limited(exc):
        """
        A rejected request still leaves a trace.

        ⚠️ An attack that shows up only as an absence is one you'll never find.
        """
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            payload = {}
        audit.log_rejection(
            creator_id=payload.get("creator_id", "unknown"),
            reason="rate_limited",
            limit=str(exc.description),
        )
        return jsonify({
            "error": "rate_limited",
            "message": "Too many submissions. Try again shortly.",
            "limit": str(exc.description),
        }), 429


# ── The worked example. Already works. Don't edit. ────────────────────────────

@app.post("/ping")
def ping():
    """
    Everything a route needs, in six lines.

    JSON arrives as a dict. You pull things out of it. You return a dict and
    the framework turns it into a response. That's the whole idea.
    """
    payload = request.get_json(silent=True) or {}
    return jsonify({
        "ok": True,
        "you_sent": payload.get("message"),
        "service": "provenance-guard",
    })


@app.get("/health")
def health():
    """Is the service up, and has the model been downloaded yet?"""
    import detector

    loaded = detector._model is not None
    return jsonify({
        "ok": True,
        "detector_model": config.DETECTOR_MODEL,
        "detector_loaded": loaded,
        "rate_limiting": config.RATE_LIMITING_ENABLED,
        "log_entries": len(audit.read_entries()),
    })


# ── The two routes built in this project ──────────────────────────────────────

@app.post("/submit")
@limiter.limit(f"{config.RATE_LIMIT_PER_MINUTE}/minute;{config.RATE_LIMIT_PER_DAY}/day")
def submit():
    """
    Take a piece of text, decide about it, log the decision, answer.

    Expects JSON:  {"text": "...", "creator_id": "..."}

    Returns 200 with content_id, guess, confidence, label, model_score,
    style_score and status. Bad input gets a 400 with an error code, and the
    refusal is written to the audit log with audit.log_rejection.
    """
    payload = request.get_json(silent=True)
    problem = _check_submission(payload)
    if problem:
        return problem

    text = payload["text"]
    creator_id = payload["creator_id"].strip()
    content_id = str(uuid.uuid4())

    import detector
    import scoring
    import stylometry

    # Unit 8 improvement: text mostly in a non-Latin script (Arabic, Chinese…)
    # is outside what either signal can read, so don't score it — answer
    # "unsure" and say so in the log, instead of a confident wrong label.
    if latin_share(text) < config.MIN_LATIN_SHARE:
        audit.log_decision(
            content_id=content_id,
            creator_id=creator_id,
            guess="unsure",
            label=scoring.LABEL_UNSURE,
            status="decided",
            text_chars=len(text),
            reason="unsupported_script",
        )
        return jsonify({
            "content_id": content_id,
            "guess": "unsure",
            "confidence": None,
            "label": scoring.LABEL_UNSURE,
            "model_score": None,
            "style_score": None,
            "status": "decided",
            "note": "not scored: mostly non-Latin script",
        })

    # Signal one — the local language model.
    try:
        model_score = detector.model_signal(text)
    except ValueError as exc:  # too few tokens for the model to score
        return _reject(creator_id, "text_too_short", str(exc))
    except detector.DetectorUnavailable as exc:
        return _reject(creator_id, "detector_unavailable", str(exc), status=503)

    # Signal two — the shape of the text.
    style_score = stylometry.style_signal(text)

    # One number, then words.
    combined = scoring.combine_signals(model_score, style_score)
    guess, label = scoring.score_to_label(combined)

    audit.log_decision(
        content_id=content_id,
        creator_id=creator_id,
        guess=guess,
        model_score=model_score,
        style_score=style_score,
        combined_score=combined,
        label=label,
        status="decided",
        text_chars=len(text),
    )

    return jsonify({
        "content_id": content_id,
        "guess": guess,
        "confidence": combined,
        "label": label,
        "model_score": model_score,
        "style_score": style_score,
        "status": "decided",
    })


def latin_share(text):
    """Share of the letters in text that are Latin letters (0.0 – 1.0)."""
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return 1.0
    latin = sum(1 for c in letters if unicodedata.name(c, "").startswith("LATIN"))
    return latin / len(letters)


def _reject(creator_id, error, message, status=400):
    """Refuse a request AND leave a trace of it in the audit log."""
    audit.log_rejection(
        creator_id=creator_id if isinstance(creator_id, str) and creator_id.strip() else "unknown",
        reason=error,
        http_status=status,
    )
    return jsonify({"error": error, "message": message}), status


def _check_submission(payload):
    """Return a 400 response if the submission is unusable, else None."""
    if not isinstance(payload, dict):
        return _reject("unknown", "invalid_json",
                       "Send a JSON object like {\"text\": \"...\", \"creator_id\": \"...\"}.")

    creator_id = payload.get("creator_id")
    text = payload.get("text")

    if not isinstance(creator_id, str) or not creator_id.strip():
        return _reject("unknown", "missing_creator_id",
                       "creator_id is required and must be a non-empty string.")
    if text is None:
        return _reject(creator_id, "missing_text", "text is required.")
    if not isinstance(text, str):
        return _reject(creator_id, "text_not_string", "text must be a string.")
    if not text.strip():
        return _reject(creator_id, "empty_text", "text is empty.")
    if len(text) > config.MAX_TEXT_CHARS:
        return _reject(creator_id, "text_too_long",
                       f"text is over {config.MAX_TEXT_CHARS} characters.")
    # Unit 8 improvement: count real words (runs of letters), not anything
    # between spaces — "!!! ??? ..." used to pass as 8 words and get a label.
    if len(re.findall(r"[^\W\d_]+", text)) < config.MIN_WORDS:
        return _reject(creator_id, "text_too_short",
                       f"text needs at least {config.MIN_WORDS} real words to be scored.")
    return None


@app.post("/appeal")
def appeal():
    """
    A writer says we got it wrong.

    Expects JSON:  {"content_id": "...", "reasoning": "..."}

    Checks the content_id exists, records the appeal next to the original
    decision with audit.log_appeal (status -> under_review), and confirms.
    400 if a field is missing, 404 if the content_id was never decided.
    """
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return _reject("unknown", "invalid_json",
                       "Send a JSON object like {\"content_id\": \"...\", \"reasoning\": \"...\"}.")

    content_id = payload.get("content_id")
    reasoning = payload.get("reasoning")
    if not isinstance(content_id, str) or not content_id.strip():
        return _reject("unknown", "missing_content_id", "content_id is required.")
    if not isinstance(reasoning, str) or not reasoning.strip():
        return _reject("unknown", "missing_reasoning",
                       "Please tell us why you think the decision is wrong.")

    content_id = content_id.strip()
    decisions = [e for e in audit.entries_for(content_id) if e.get("guess") is not None]
    if not decisions:
        audit.log_rejection(creator_id="unknown", reason="unknown_content_id",
                            content_id=content_id, http_status=404)
        return jsonify({"error": "not_found",
                        "message": f"No submission with content_id {content_id}."}), 404

    original = decisions[-1]
    audit.log_appeal(content_id=content_id,
                     creator_id=original.get("creator_id", "unknown"),
                     reasoning=reasoning.strip())

    return jsonify({
        "content_id": content_id,
        "status": "under_review",
        "message": "Thanks — your appeal is recorded and a person will review "
                   "this decision. The original label stays until then.",
    })


# ── Already works ─────────────────────────────────────────────────────────────

@app.get("/log")
def get_log():
    """
    The audit log, most recent last.

        curl "http://127.0.0.1:5000/log?limit=10"

    You need this in unit 8 to paste entries into your README, and you need it
    now to see whether your logging is actually working.
    """
    limit = request.args.get("limit", type=int)
    entries = audit.read_entries(limit=limit)
    return jsonify({"count": len(entries), "entries": entries})


def main():
    print(f"Provenance Guard on http://{config.HOST}:{config.PORT}")
    print(f"  detector model:  {config.DETECTOR_MODEL}")
    print(f"  rate limiting:   {'ON' if config.RATE_LIMITING_ENABLED else 'off (unit 8)'}")
    print(f"  audit log:       {config.AUDIT_LOG}")
    print()
    print("Check it's alive:")
    print(f'  curl -X POST http://{config.HOST}:{config.PORT}/ping \\')
    print('    -H "Content-Type: application/json" \\')
    print("    -d '{\"message\": \"hello\"}'")
    print()
    # debug=True hands out an interactive debugger, so it's local-only — see config.py
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)


if __name__ == "__main__":
    main()
