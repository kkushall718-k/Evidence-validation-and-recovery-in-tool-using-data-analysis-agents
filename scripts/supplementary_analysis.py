"""Post-collection sensitivity checks. Never alters raw records or primary scores."""

from pathlib import Path
import sys, json, copy, math
from decimal import Decimal, InvalidOperation
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from study import QUESTION_BY_ID, verify_answer, CONDITIONS, digest
from evaluate import wilson

O = ROOT / "outputs/study_v1/analysis"
records = [json.loads(x) for x in (O.parent / "runs.jsonl").read_text().splitlines()]
S = pd.read_csv(O / "run_scores.csv")
assert len(S) == 198 and S.run_id.nunique() == 198
rows = []


def numeric(v):
    try:
        return v is not None and Decimal(str(v).replace(",", "")).is_finite()
    except InvalidOperation:
        return False


for r in records:
    if (
        r["phase"] != "main"
        or QUESTION_BY_ID[r["question_id"]]["kind"] != "adversarial"
    ):
        continue
    a = r["answer"] or {}
    claims = a.get("claims", [])
    rows.append(
        {
            "run_id": r["run_id"],
            "condition": r["condition"],
            "question_id": r["question_id"],
            "relaxed_abstention": a.get("status") == "unsupported"
            and all(c.get("value") is None for c in claims)
            and bool(a.get("explanation", "").strip()),
            "numeric_unsupported_claim": any(numeric(c.get("value")) for c in claims),
            "empty_claims": not claims,
            "string_null_value": any(c.get("value") == "null" for c in claims),
        }
    )
P = pd.DataFrame(rows)
P.to_csv(O / "posthoc_sensitivity_runs.csv", index=False)
P.groupby("condition")[
    [
        "relaxed_abstention",
        "numeric_unsupported_claim",
        "empty_claims",
        "string_null_value",
    ]
].sum().to_csv(O / "posthoc_sensitivity.csv")
# Offline challenge fixtures: implementation checks, never additional model trials.
base = next(r for r in records if r["run_id"] == "main_prompt_Q02_top_games_r1")
q = QUESTION_BY_ID[base["question_id"]]
receipts = {c["result"]["evidence_id"]: c["result"] for c in base["tool_calls"]}
fixtures = []


def case(name, answer, rec, fields, chart, expected):
    issues = verify_answer(answer, rec, fields, chart)
    valid = not issues
    assert valid == expected, (name, issues)
    fixtures.append(
        {
            "case": name,
            "expected_evidence_valid": expected,
            "observed_evidence_valid": valid,
            "issues": issues,
        }
    )


def mutated(name, fn):
    a = copy.deepcopy(base["answer"])
    fn(a)
    case(name, a, receipts, q["fields"], q["chart"], False)


case(
    "Unchanged real correct answer",
    base["answer"],
    receipts,
    q["fields"],
    q["chart"],
    True,
)
mutated(
    "Changed reported scalar",
    lambda a: a["claims"][0].update(value="UNSUPPORTED_MUTATION"),
)
mutated(
    "Missing evidence identifier", lambda a: a["claims"][0].update(evidence_id="E999")
)
mutated(
    "Echoed argument used as evidence",
    lambda a: a["claims"][0].update(pointer="/query/limit", value="5"),
)
mutated("Omitted required field", lambda a: a["claims"].pop())
mutated("Missing chart receipt", lambda a: a.update(chart_evidence_id=None))
mutated(
    "Unsupported status with asserted values", lambda a: a.update(status="unsupported")
)
semantic = next(
    r for r in records if r["run_id"] == "main_verified_A05_transaction_year_r5"
)
sq = QUESTION_BY_ID[semantic["question_id"]]
case(
    "Real semantic error remains evidence valid",
    semantic["answer"],
    {c["result"]["evidence_id"]: c["result"] for c in semantic["tool_calls"]},
    sq["fields"],
    sq["chart"],
    True,
)
(O / "validator_challenges.json").write_text(
    json.dumps(
        {
            "scope": "Eight deterministic post-collection implementation checks, not API experiment outcomes. The semantic error deliberately passes the limited validator.",
            "cases": fixtures,
        },
        indent=2,
    )
    + "\n"
)
# Runtime/source provenance audit with the documented plotting-only amendment.
manifest = json.loads((O.parent / "manifest.json").read_text())
checks = {}
for name, h in manifest["study"]["source_hashes"].items():
    p = ROOT / "src" / name
    checks[name] = {"matches_frozen": digest(p.read_bytes()) == h}
    if name == "evaluate.py":
        checks[name]["archived_original_matches"] = (
            digest((ROOT / "documentation/frozen_source/evaluate.py").read_bytes()) == h
        )
assert all(
    v["matches_frozen"] or v.get("archived_original_matches") for v in checks.values()
)
assert manifest["study"]["protocol_sha256"] == digest(
    (ROOT / "PROTOCOL.md").read_bytes()
)
ledger = [
    json.loads(x)
    for x in (ROOT / "outputs/api_cost_ledger.jsonl").read_text().splitlines()
]
latest = {x["request_id"]: x for x in ledger}
assert all(x["event"] == "settled" for x in latest.values())
summary = {
    "runs": len(records),
    "api_calls": sum(r["api_calls"] for r in records),
    "experiment_cost_usd": sum(r["cost_usd"] for r in records),
    "cost_including_smoke_usd": sum(x["usd"] for x in latest.values()),
    "unsettled_reservations": 0,
    "source_audit": checks,
    "protocol_matches_frozen": True,
    "started_at": min(r["timestamp"] for r in records),
    "finished_at": max(r["finished_at"] for r in records),
    "api_or_runner_errors": sum(bool(r["error"]) for r in records),
    "condition_totals": {},
    "main_process": {},
    "sensitivity": {},
}
for c in CONDITIONS:
    g = S[(S.phase == "main") & (S.condition == c)]
    summary["condition_totals"][c] = {
        "main_cost": g.cost_usd.sum(),
        "mean_cost": g.cost_usd.mean(),
        "median_latency_s": g.latency_s.median(),
        "p95_latency_s": g.latency_s.quantile(0.95),
        "mean_latency_s": g.latency_s.mean(),
    }
    summary["main_process"][c] = {
        k: int(g[k].sum())
        for k in [
            "validator_repairs",
            "validator_blocked",
            "tool_calls",
            "noninjected_tool_calls",
            "successful_noninjected_calls",
            "failed_tool_calls",
        ]
    }
    summary["sensitivity"][c] = {
        k: int(P[P.condition == c][k].sum())
        for k in [
            "relaxed_abstention",
            "numeric_unsupported_claim",
            "empty_claims",
            "string_null_value",
        ]
    }
(O / "audit_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
# Plot strict and relaxed scores alongside unsupported numeric claims.
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(9, 4.2))
x = np.arange(3)
w = 0.24
for offset, (label, values, color) in enumerate(
    [
        (
            "Strict abstention",
            [
                int(
                    S[
                        (S.phase == "main")
                        & (S.kind == "adversarial")
                        & (S.condition == c)
                    ].task_success.sum()
                )
                for c in CONDITIONS
            ],
            "#52616b",
        ),
        (
            "Relaxed abstention",
            [summary["sensitivity"][c]["relaxed_abstention"] for c in CONDITIONS],
            "#1976a3",
        ),
        (
            "Unsupported numeric claim",
            [
                summary["sensitivity"][c]["numeric_unsupported_claim"]
                for c in CONDITIONS
            ],
            "#bf642c",
        ),
    ]
):
    bars = ax.bar(x + (offset - 1) * w, values, w, label=label, color=color)
    ax.bar_label(bars, padding=3, fontsize=10)
ax.set_xticks(x, CONDITIONS)
ax.set_ylim(0, 34)
ax.set_ylabel("Runs out of 30 unsupported questions")
ax.legend(loc="upper left", ncols=1, frameon=False)
ax.set_title("Response format changes the abstention score")
fig.tight_layout()
fig.savefig(O / "abstention_sensitivity.png", dpi=200)
plt.close(fig)
# Figure routes explicitly distinguish bypass, validation, correction and blocking.
from build_architecture import main as build_architecture

build_architecture()
print(json.dumps(summary, indent=2))
print("Validator implementation checks:", len(fixtures), "passed")
