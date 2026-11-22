#!/usr/bin/env python3
"""Validate data/ai_model_releases.csv. Usage: python3 scripts/check_dataset.py [path]. Exit 1 on any error."""
import csv, re, sys
from datetime import date

path = sys.argv[1] if len(sys.argv) > 1 else "data/ai_model_releases.csv"
rows = list(csv.DictReader(open(path, encoding="utf-8")))
DATES = ["announced", "first_available", "general_availability", "api_available", "open_weights", "retired_on", "count_date", "count_date_any_stage"]
STAGES = {"ga", "open_weights_release", "preview", "beta", "experimental", "gated"}
errors = []

def err(r, msg):
    errors.append(f"{r['model_id']}: {msg}")

def d(v):
    return date.fromisoformat(v) if re.fullmatch(r"\d{4}-\d{2}-\d{2}", v or "") else None

ids = [r["model_id"] for r in rows]
if len(ids) != len(set(ids)):
    errors.append("duplicate model_id values")
for r in rows:
    for c in DATES:
        if r[c] and d(r[c]) is None:
            err(r, f"{c} is not an ISO date: {r[c]!r}")
    if r["stage_at_launch"] not in STAGES:
        err(r, f"unknown stage {r['stage_at_launch']!r}")
    if r["confidence"] not in {"high", "medium", "low"}:
        err(r, f"unknown confidence {r['confidence']!r}")
    if not r["vendor_page"].startswith("http"):
        err(r, "missing vendor_page URL")
    if r["counted_strict"] not in {"0", "1"}:
        err(r, "counted_strict must be 0 or 1")
    if r["counted_strict"] == "1":
        cd = d(r["count_date"])
        if not cd:
            err(r, "counted but no count_date")
        elif not (date(2023, 3, 14) <= cd <= date(2026, 11, 22)):
            err(r, f"count_date outside window: {cd}")
    elif not r["reason_not_counted"]:
        err(r, "not counted but no reason_not_counted")
    fa, ga, ret = d(r["first_available"]), d(r["general_availability"]), d(r["retired_on"])
    if fa and ga and ga < fa:
        err(r, "general_availability before first_available")
    if fa and ret and ret < fa:
        err(r, "retired_on before first_available")
    for c in ("input_usd_per_1m_tokens", "output_usd_per_1m_tokens", "context_window_tokens"):
        if r[c]:
            try:
                float(r[c])
            except ValueError:
                err(r, f"{c} is not numeric")
print(f"{len(rows)} rows, {sum(r['counted_strict'] == '1' for r in rows)} counted (strict), {len(errors)} errors")
for e in errors:
    print(" -", e)
sys.exit(1 if errors else 0)
