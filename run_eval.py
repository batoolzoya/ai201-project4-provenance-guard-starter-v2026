#!/usr/bin/env python3
"""
Run your five criteria three times each.  <- UNIT 8, MILESTONE 3

    python app.py                              # in one terminal
    python run_eval.py --label before          # in another
    python run_eval.py --label after

The attack set tests what staff thought to test. This tests what *you* thought
to test, and the two rarely overlap much. Both count.

Fill in `scenarios.py` first — that's where you say what each criterion needs
run against it. A criterion about false positives needs your own writing. One
about label coverage needs inputs across the score range.

Three trials. Neither signal is random, so identical input should score
identically; the repeats show the result holds.

This does the sending and the recording. It does not decide whether a trial
passed — that depends on the criterion you wrote, so the Verdict column comes
back blank.
"""

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

import config

# Windows consoles often run a codepage that can't print every character in
# this file's help text. Without this, `--help` ends in a UnicodeEncodeError
# traceback instead of the help — which is a miserable first thing to hit.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(errors="replace")
    except (AttributeError, ValueError):  # not a normal text stream
        pass


DEFAULT_URL = f"http://{config.HOST}:{config.PORT}"


def bodies_for(scenario):
    """
    The request bodies one scenario sends.

    A "texts" scenario gets a creator_id made up for it. A "bodies" scenario is
    sent exactly as written, which is how a bad-input criterion says things a
    string can't — no `text` field, a null, something enormous.
    """
    if scenario.get("bodies"):
        return list(scenario["bodies"])
    return [
        {"text": text, "creator_id": f"eval_{scenario['name'][:12]}_{i}"}
        for i, text in enumerate(scenario["texts"], 1)
    ]


def run_submissions(requests, args, scenario):
    """Send every body in one scenario once. Returns one result per body."""
    names = scenario.get("names") or []
    results = []
    for i, body in enumerate(bodies_for(scenario)):
        preview = names[i] if i < len(names) else describe(body)
        try:
            response = requests.post(f"{args.url}/submit", json=body,
                                     timeout=args.timeout)
            payload = response.json() if response.content else {}
            results.append({
                "sent": preview,
                "status": response.status_code,
                "guess": payload.get("guess"),
                "confidence": payload.get("confidence"),
                "model_score": payload.get("model_score"),
                "style_score": payload.get("style_score"),
                "error": payload.get("error"),
            })
        except Exception as exc:  # noqa: BLE001
            results.append({"sent": preview, "status": None,
                            "error": f"{type(exc).__name__}: {exc}"})
    return results


def submission_summary(scenario, results):
    """Counts only — whether that meets the criterion is my call, not this script's."""
    guesses = [r.get("guess") for r in results]
    statuses = [r.get("status") for r in results]
    parts = [f"ai={guesses.count('ai')} unsure={guesses.count('unsure')} "
             f"human={guesses.count('human')}"]
    if any(s != 200 for s in statuses):
        parts.append("statuses=" + ",".join(str(s) for s in statuses))
    for group, indexes in (scenario.get("groups") or {}).items():
        scores = [results[i].get("confidence") for i in indexes]
        if all(isinstance(x, (int, float)) for x in scores):
            parts.append(f"mean[{group}]={sum(scores) / len(scores):.3f}")
    return " · ".join(parts)


def run_appeals(requests, args, scenario, trial):
    """
    Criterion 4: submit each text, appeal the content_id that came back, then
    read the audit log to see whether that id's latest status is under_review.
    Ends with one appeal against a made-up content_id, which should be 404.
    """
    results = []
    for i, text in enumerate(scenario["appeal_texts"], 1):
        result = {"sent": f"appeal test #{i}"}
        try:
            sub = requests.post(f"{args.url}/submit", timeout=args.timeout,
                                json={"text": text,
                                      "creator_id": f"eval_appeal_{i}"})
            result["submit_status"] = sub.status_code
            content_id = sub.json().get("content_id")
            result["content_id"] = content_id
            app = requests.post(f"{args.url}/appeal", timeout=args.timeout,
                                json={"content_id": content_id,
                                      "reasoning": f"Eval trial {trial}: I wrote this myself."})
            result["appeal_status"] = app.status_code
            entries = requests.get(f"{args.url}/log", timeout=args.timeout).json()["entries"]
            mine = [e for e in entries if e.get("content_id") == content_id]
            result["log_status_after"] = mine[-1].get("status") if mine else None
            result["log_has_appeal_entry"] = any(e.get("event") == "appeal" for e in mine)
        except Exception as exc:  # noqa: BLE001
            result["error"] = f"{type(exc).__name__}: {exc}"
        results.append(result)

    fake = f"made-up-id-trial-{trial}"
    try:
        app = requests.post(f"{args.url}/appeal", timeout=args.timeout,
                            json={"content_id": fake, "reasoning": "testing"})
        results.append({"sent": "appeal with a made-up content_id",
                        "content_id": fake, "appeal_status": app.status_code})
    except Exception as exc:  # noqa: BLE001
        results.append({"sent": "appeal with a made-up content_id",
                        "error": f"{type(exc).__name__}: {exc}"})
    return results


def count_rejections(requests, args):
    """How many 'rejected' entries the audit log holds right now."""
    entries = requests.get(f"{args.url}/log", timeout=args.timeout).json()["entries"]
    return sum(1 for e in entries if e.get("event") == "rejected")


def appeal_summary(results):
    real = [r for r in results if r.get("sent", "").startswith("appeal test")]
    ok = sum(1 for r in real if r.get("appeal_status") == 200
             and r.get("log_status_after") == "under_review"
             and r.get("log_has_appeal_entry"))
    fake = results[-1].get("appeal_status")
    return f"{ok}/{len(real)} appeals 200 + under_review in log · made-up id -> {fake}"


def describe(body):
    """A short, readable note of what was sent — for the report."""
    if set(body) == {"text", "creator_id"} and isinstance(body.get("text"), str):
        text = body["text"]
        return text[:70] if text else "(empty text)"
    return json.dumps(body)[:120]


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--label", default="")
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--timeout", type=float, default=90.0)
    args = parser.parse_args()

    try:
        import requests
    except ImportError:
        print("The `requests` package isn't installed.\n"
              "Run: pip install -r requirements.txt", file=sys.stderr)
        sys.exit(1)

    try:
        import scenarios
    except ImportError:
        print("No scenarios.py found. Milestone 3 starts by filling it in.",
              file=sys.stderr)
        sys.exit(1)

    problems = scenarios.validate()
    if problems:
        print("scenarios.py has problems:\n", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        sys.exit(1)

    try:
        requests.get(f"{args.url}/health", timeout=5)
    except Exception:  # noqa: BLE001
        print(f"Nothing answering at {args.url}. Start it:  python app.py",
              file=sys.stderr)
        sys.exit(1)

    if args.trials < 3:
        print(f"!! {args.trials} trial(s). The submission asks for three.\n")

    rows = []
    for scenario in scenarios.SCENARIOS:
        print(f"\n{scenario['name']}  (criterion {scenario.get('criterion') or '—'})")

        trials = []
        for trial in range(1, args.trials + 1):
            if scenario.get("appeal_texts"):
                results = run_appeals(requests, args, scenario, trial)
                summary = appeal_summary(results)
            else:
                rejected_before = count_rejections(requests, args)
                results = run_submissions(requests, args, scenario)
                summary = submission_summary(scenario, results)
                if scenario.get("bodies"):
                    added = count_rejections(requests, args) - rejected_before
                    summary += f" · new 'rejected' log entries={added}"
            trials.append({"summary": summary, "results": results})
            print(f"  trial {trial}: {summary}")

        rows.append({"scenario": scenario, "trials": trials})

    write_report(rows, args)


def write_report(rows, args):
    config.RESULTS_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    label = f"_{args.label}" if args.label else ""
    path = config.RESULTS_DIR / f"run_{stamp}{label}.md"

    n = args.trials
    headers = " | ".join(f"Run {i}" for i in range(1, n + 1))
    divider = "|".join(["---"] * n)

    lines = [
        f"# Run log{f' — {args.label}' if args.label else ''}",
        "",
        "- Produced by: `run_eval.py::main`",
        "- Service: `app.py::submit` · scoring: `scoring.py::combine_signals`",
        f"- {n} trials per criterion · {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "Fill in Target from `criteria.md`, and Run and Verdict from the output",
        "underneath. Whether a trial passed depends on the criterion you wrote.",
        "",
        f"| Criterion | Target | {headers} | Verdict |",
        f"|---|---|{divider}|---|",
    ]

    for row in rows:
        scenario = row["scenario"]
        number = scenario.get("criterion")
        name = f"{number}. {scenario['name']}" if number else scenario["name"]
        lines.append(f"| {name} |  | {' | '.join([' '] * n)} |  |")

    lines += ["", "## Per-trial counts (facts, not verdicts)", ""]
    for row in rows:
        scenario = row["scenario"]
        lines.append(f"**{scenario.get('criterion')}. {scenario['name']}**")
        lines.append("")
        for t, trial in enumerate(row["trials"], 1):
            lines.append(f"- Trial {t}: {trial['summary']}")
        lines.append("")

    lines += ["---", "", "## What actually came back", "",
              "Real output. My own writing shows as \"my piece #N\" — the text",
              "itself stays in the git-ignored private/ folder.", ""]

    for row in rows:
        scenario = row["scenario"]
        lines += [f"### {scenario['name']}", ""]
        for trial_number, trial in enumerate(row["trials"], 1):
            lines += [f"**Trial {trial_number}** — {trial['summary']}", "", "```json",
                      json.dumps(trial["results"], indent=2), "```", ""]

    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {path.relative_to(config.ROOT)}")
    print("Commit it. It's the evidence the test actually happened.")


if __name__ == "__main__":
    main()
