"""Independent review of supplied evidence; no project evaluation helpers or API calls."""

from pathlib import Path
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation
from datetime import datetime
import csv, json, hashlib, zipfile, math, statistics

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / ".build/evidence_verification"
OUT.mkdir(parents=True, exist_ok=True)


def readj(p):
    return json.loads(p.read_text())


def lines(p):
    return [json.loads(s) for s in p.read_text().splitlines() if s.strip()]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def eqnum(a, b, tol=Decimal(".005")):
    try:
        x, y = Decimal(str(a).replace(",", "")), Decimal(str(b))
        return x.is_finite() and y.is_finite() and abs(x - y) <= tol
    except (InvalidOperation, TypeError):
        return False


def eq(a, b):
    if isinstance(b, (Decimal, int, float)):
        return eqnum(a, b, Decimal(0) if isinstance(b, int) else Decimal(".005"))
    return isinstance(a, str) and a.strip().casefold() == b.strip().casefold()


def numeric(a):
    try:
        return a is not None and Decimal(str(a).replace(",", "")).is_finite()
    except InvalidOperation:
        return False


M = readj(ROOT / "outputs/study_v1/manifest.json")
m = M["study"]
assert (
    sha(json.dumps(m, sort_keys=True, ensure_ascii=False).encode()) == M["study_sha256"]
)
assert sha((ROOT / "data/vgsales.csv").read_bytes()) == m["dataset_sha256"]
assert sha((ROOT / "PROTOCOL.md").read_bytes()) == m["protocol_sha256"]
source_checks = {}
for name, h in m["source_hashes"].items():
    matches = sha((ROOT / "src" / name).read_bytes()) == h
    archived = (
        name == "evaluate.py"
        and sha((ROOT / "documentation/frozen_source/evaluate.py").read_bytes()) == h
    )
    assert matches or archived
    source_checks[name] = {
        "current_matches": matches,
        "archived_matches": bool(archived),
    }
R = lines(ROOT / "outputs/study_v1/runs.jsonl")
plan = {x["run_id"]: x for x in m["plan"]}
assert len(R) == len(plan) == 198 and len({r["run_id"] for r in R}) == 198
assert {r["run_id"] for r in R} == set(plan)
assert [r["run_id"] for r in R] == [p["run_id"] for p in m["plan"]]
L = lines(ROOT / "outputs/api_cost_ledger.jsonl")
latest = {x["request_id"]: x for x in L}
assert all(x["event"] == "settled" for x in latest.values())
ledger = {x["response_id"]: x for x in latest.values()}
assert len(ledger) == len(latest)
seen = []
tool_calls = 0
pngs = set()
for r in R:
    assert readj(ROOT / "outputs/study_v1/runs" / r["run_id"] / "record.json") == r
    for k, v in plan[r["run_id"]].items():
        assert r[k] == v
    assert r["model"] == m["model"] and r["temperature"] == m["temperature"]
    assert r["dataset_sha256"] == m["dataset_sha256"]
    assert r["system_prompt_sha256"] == sha(m["prompts"][r["condition"]].encode())
    assert (
        datetime.fromisoformat(M["frozen_at"])
        < datetime.fromisoformat(r["timestamp"])
        <= datetime.fromisoformat(r["finished_at"])
    )
    assert r["api_calls"] == len(r["trace"])
    sums = defaultdict(float)
    function_calls = []
    for t in r["trace"]:
        seen.append(t["response_id"])
        e = ledger[t["response_id"]]
        assert (
            e["run_id"] == r["run_id"]
            and e["usage"] == t["usage"]
            and t["status"] == "completed"
        )
        u = t["usage"]
        cached = u.get("input_tokens_details", {}).get("cached_tokens", 0)
        prices = m["prices_per_million_tokens"]
        cost = (
            (u["input_tokens"] - cached) * prices["input"]
            + cached * prices["cached_input"]
            + u["output_tokens"] * prices["output"]
        ) / 1e6
        assert math.isclose(cost, e["usd"], abs_tol=1e-12) and math.isclose(
            cost, t["cost_usd"], abs_tol=1e-12
        )
        for k in ("input_tokens", "output_tokens"):
            sums[k] += u[k]
        sums["cached_input_tokens"] += cached
        sums["cost_usd"] += cost
        function_calls.extend(x for x in t["output"] if x["type"] == "function_call")
    assert all(math.isclose(r[k], v, abs_tol=1e-10) for k, v in sums.items())
    assert len(function_calls) == len(r["tool_calls"])
    for api, c in zip(function_calls, r["tool_calls"]):
        assert (
            api["name"] == c["name"] and json.loads(api["arguments"]) == c["arguments"]
        )
        assert c["ok"] == c["result"]["ok"]
        if c["name"] == "plot" and c["ok"]:
            p = Path(c["result"]["chart_file"])
            assert not p.is_absolute()
            p = ROOT / p
            assert p.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
            pngs.add(str(p.relative_to(ROOT)))
    final = "\n".join(
        c["text"]
        for t in r["trace"][-1:]
        for item in t["output"]
        if item["type"] == "message"
        for c in item["content"]
        if c["type"] == "output_text"
    )
    assert final == r["raw_final_text"] and json.loads(final) == r["answer"]
    tool_calls += len(r["tool_calls"])
assert len(seen) == len(set(seen)) == 583
assert {e["response_id"] for e in latest.values() if e["run_id"] in plan} == set(seen)

with (ROOT / "data/vgsales.csv").open(encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))
na = ("", "N/A", "NaN")
D = Decimal
year = lambda r: None if r["Year"] in na else int(D(r["Year"]))
top = sorted(rows, key=lambda r: (-D(r["Global_Sales"]), int(r["Rank"])))[:5]
annual = defaultdict(Decimal)
pub = defaultdict(Decimal)
regional = {c: defaultdict(Decimal) for c in ("NA_Sales", "EU_Sales", "JP_Sales")}
subset = []
for r in rows:
    y = year(r)
    if y is not None:
        annual[y] += D(r["Global_Sales"])
        if 2000 <= y <= 2009 and r["Publisher"] not in na:
            pub[r["Publisher"]] += D(r["Global_Sales"])
        if 2005 <= y <= 2010 and r["Publisher"] == "Nintendo" and r["Platform"] == "DS":
            subset.append(r)
    for c in regional:
        regional[c][r["Genre"]] += D(r[c])
peak = sorted(annual, key=lambda y: (-annual[y], y))[0]
pubs = sorted(pub, key=lambda p: (-pub[p], p))[:5]
T = {
    "Q01_quality": dict(
        missing_year_rows=sum(year(r) is None for r in rows),
        out_of_range_year_rows=sum(
            year(r) is not None and not 1980 <= year(r) <= 2016 for r in rows
        ),
        missing_publisher_rows=sum(r["Publisher"] in na for r in rows),
    ),
    "Q02_top_games": dict(
        top_game_name=top[0]["Name"],
        top_game_platform=top[0]["Platform"],
        top_game_global_sales=D(top[0]["Global_Sales"]),
        second_game_name=top[1]["Name"],
        second_game_global_sales=D(top[1]["Global_Sales"]),
    ),
    "Q03_release_year": dict(
        peak_release_year=peak, peak_release_year_global_sales=annual[peak]
    ),
    "Q04_regions": {},
    "Q05_filtered": dict(
        matching_rows=len(subset),
        global_sales_total=sum(D(r["Global_Sales"]) for r in subset),
    ),
    "Q06_publishers": dict(
        top_publisher=pubs[0], top_publisher_global_sales=pub[pubs[0]]
    ),
}
for prefix, c in [("na", "NA_Sales"), ("eu", "EU_Sales"), ("jp", "JP_Sales")]:
    g = sorted(regional[c], key=lambda g: (-regional[c][g], g))[0]
    T["Q04_regions"].update(
        {prefix + "_top_genre": g, prefix + "_top_genre_sales": regional[c][g]}
    )
charts = {
    "Q02_top_games": (
        "bar",
        "Name",
        ["Global_Sales"],
        [{k: r[k] for k in ("Name", "Global_Sales")} for r in top],
    ),
    "Q03_release_year": (
        "line",
        "Year",
        ["Global_Sales"],
        [dict(Year=y, Global_Sales=annual[y]) for y in sorted(annual)],
    ),
    "Q04_regions": (
        "bar",
        "Genre",
        list(regional),
        [
            dict(Genre=g, **{c: regional[c][g] for c in regional})
            for g in sorted(regional["NA_Sales"])
        ],
    ),
    "Q06_publishers": (
        "bar",
        "Publisher",
        ["Global_Sales"],
        [dict(Publisher=p, Global_Sales=pub[p]) for p in pubs],
    ),
}
questions = {q["id"]: q for q in m["questions"]}


def chart_ok(r):
    kind, x, ys, expected = charts[r["question_id"]]
    c = next(
        c["result"]
        for c in r["tool_calls"]
        if c["result"]["evidence_id"] == r["answer"]["chart_evidence_id"]
    )
    if (
        c["kind"] != kind
        or c["x"] != x
        or set(c["ys"]) != set(ys)
        or len(c["rows"]) != len(expected)
    ):
        return False
    key = lambda v: float(v) if x == "Year" else str(v)
    got = {key(row[x]): row for row in c["rows"]}
    if len(got) != len(expected):
        return False
    if not all(
        key(row[x]) in got and all(eqnum(got[key(row[x])][y], row[y]) for y in ys)
        for row in expected
    ):
        return False
    if kind == "line" and [float(row[x]) for row in c["rows"]] != sorted(
        float(row[x]) for row in c["rows"]
    ):
        return False
    return True


summary = {}
independently_scored = {}
variance = []
for condition in ("baseline", "prompt", "verified"):
    main = [r for r in R if r["phase"] == "main" and r["condition"] == condition]
    counts = Counter()
    outcome_groups = defaultdict(list)
    for r in [r for r in R if r["condition"] == condition]:
        q = questions[r["question_id"]]
        a = r["answer"]
        cl = a["claims"]
        values = {c["field"]: c["value"] for c in cl}
        contract = len(cl) == len(q["fields"]) and set(values) == set(q["fields"])
        if q["kind"] == "answerable":
            correct = sum(eq(values.get(f), v) for f, v in T[q["id"]].items())
            chart = chart_ok(r) if q["chart"] else True
            success = (
                contract
                and a["status"] == "answered"
                and correct == len(T[q["id"]])
                and chart
            )
            if r["phase"] == "main":
                counts.update(
                    answerable_runs=1,
                    answerable_success=int(success),
                    correct_fields=correct,
                    requested_fields=len(T[q["id"]]),
                    charts=int(q["chart"]),
                    correct_charts=int(q["chart"] and chart),
                )
        else:
            asserted = any(c["value"] is not None for c in cl)
            relaxed = (
                a["status"] == "unsupported"
                and not asserted
                and bool(a["explanation"].strip())
            )
            success = contract and relaxed
            counts.update(
                unsupported_runs=1,
                strict_abstention=int(success),
                relaxed_abstention=int(relaxed),
                nonnull_claim=int(asserted),
                numeric_claim=int(any(numeric(c["value"]) for c in cl)),
                error_status=int(a["status"] == "error"),
            )
        independently_scored[r["run_id"]] = bool(success)
        if r["phase"] == "main":
            outcome_groups[r["question_id"]].append(int(success))
        else:
            exposed = sum(bool(c["injected"]) for c in r["tool_calls"])
            assert exposed == 1
            counts.update(recovery_exposed=1, recovery_success=int(success))
    counts.update(
        main_tool_calls=sum(len(r["tool_calls"]) for r in main),
        main_tool_success=sum(c["ok"] for r in main for c in r["tool_calls"]),
        repairs=sum(r["validator_repairs"] for r in R if r["condition"] == condition),
        blocked=sum(r["validator_blocked"] for r in R if r["condition"] == condition),
    )
    summary[condition] = dict(counts)
    summary[condition].update(
        main_cost=sum(r["cost_usd"] for r in main),
        median_latency=statistics.median(r["latency_s"] for r in main),
        outcome_consistent_groups=sum(
            len(set(g)) == 1 for g in outcome_groups.values()
        ),
    )
    for q, g in outcome_groups.items():
        variance.append(
            {
                "condition": condition,
                "question_id": q,
                "n": len(g),
                "sample_variance_success": statistics.variance(g),
                "analysis_status": "post hoc review diagnostic; not added to frozen outcomes",
            }
        )
with (ROOT / "outputs/study_v1/analysis/run_scores.csv").open() as f:
    saved = list(csv.DictReader(f))
assert (
    len(saved) == 198
    and len({s["run_id"] for s in saved}) == 198
    and {s["run_id"] for s in saved} == set(independently_scored)
)
assert all(
    independently_scored[s["run_id"]] == (s["task_success"] == "True") for s in saved
)
report = {
    "scope": "Local evidence integrity and independent recomputation, not provider-side billing/authenticity certification",
    "runs": len(R),
    "unique_response_ids": len(seen),
    "ledger_settlements_including_smoke": len(latest),
    "tool_calls": tool_calls,
    "saved_chart_files": len(pngs),
    "dataset_rows": len(rows),
    "all_198_task_scores_match_independent_recomputation": True,
    "source_checks": source_checks,
    "experiment_cost": sum(r["cost_usd"] for r in R),
    "ledger_cost_including_smoke": sum(e["usd"] for e in latest.values()),
    "summary": summary,
    "task_success_sample_variance": variance,
}
(OUT / "independent_audit.json").write_text(json.dumps(report, indent=2) + "\n")
print(
    json.dumps(
        {
            k: v
            for k, v in report.items()
            if k not in ("task_success_sample_variance", "source_checks")
        },
        indent=2,
    )
)
