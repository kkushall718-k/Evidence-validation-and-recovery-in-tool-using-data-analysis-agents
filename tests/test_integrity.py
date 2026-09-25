import csv
import io
import json
import sys
import tempfile
import unittest
from collections import defaultdict
from decimal import Decimal
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import pandas as pd
from study import (
    DATASET,
    DataTools,
    verify_answer,
    scalar_equal,
    CONDITIONS,
    QUESTION_BY_ID,
)
from ground_truth import derive
from evaluate import wilson, score_run, chart_matches, validate_records
from run_experiment import Client, BudgetExceeded, APIError, planned_runs, read_jsonl


def query_args(**changes):
    a = dict(
        operation="count",
        columns=[],
        filters=[],
        filter_mode="all",
        group_by=[],
        aggregation="sum",
        sort_by=[],
        descending=False,
        limit=50,
    )
    a.update(changes)
    return a


def claim_answer(
    value, evidence="E001", pointer="/rows/0/row_count", field="matching_rows"
):
    return {
        "status": "answered",
        "claims": [
            {
                "field": field,
                "value": value,
                "evidence_id": evidence,
                "pointer": pointer,
            }
        ],
        "chart_evidence_id": None,
        "explanation": "Counted matching source rows.",
    }


class IntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.df = pd.read_csv(DATASET)
        cls.truth = derive(cls.df)

    def test_independent_csv_ground_truth(self):
        with DATASET.open(newline="", encoding="utf-8-sig") as f:
            rows = list(csv.DictReader(f))
        d = lambda x: Decimal(x)
        missyear = sum(r["Year"] in ("", "N/A", "NaN") for r in rows)
        year = lambda r: (
            None if r["Year"] in ("", "N/A", "NaN") else int(float(r["Year"]))
        )
        outside = sum(year(r) is not None and not 1980 <= year(r) <= 2016 for r in rows)
        missingpublisher = sum(r["Publisher"] in ("", "N/A", "NaN") for r in rows)
        self.assertEqual(
            self.truth["answers"]["Q01_quality"],
            dict(
                missing_year_rows=missyear,
                out_of_range_year_rows=outside,
                missing_publisher_rows=missingpublisher,
            ),
        )
        top = sorted(rows, key=lambda r: (-d(r["Global_Sales"]), int(r["Rank"])))
        expected = dict(
            top_game_name=top[0]["Name"],
            top_game_platform=top[0]["Platform"],
            top_game_global_sales=float(top[0]["Global_Sales"]),
            second_game_name=top[1]["Name"],
            second_game_global_sales=float(top[1]["Global_Sales"]),
        )
        self.assertEqual(self.truth["answers"]["Q02_top_games"], expected)
        annual = defaultdict(Decimal)
        publishers = defaultdict(Decimal)
        regions = {
            c: defaultdict(Decimal) for c in ["NA_Sales", "EU_Sales", "JP_Sales"]
        }
        subset = []
        for r in rows:
            y = year(r)
            if y is not None:
                annual[y] += d(r["Global_Sales"])
                if 2000 <= y <= 2009 and r["Publisher"] not in ("", "N/A", "NaN"):
                    publishers[r["Publisher"]] += d(r["Global_Sales"])
                if (
                    2005 <= y <= 2010
                    and r["Publisher"] == "Nintendo"
                    and r["Platform"] == "DS"
                ):
                    subset.append(r)
            for c in regions:
                regions[c][r["Genre"]] += d(r[c])
        y = max(annual, key=annual.get)
        self.assertEqual(
            self.truth["answers"]["Q03_release_year"],
            dict(peak_release_year=y, peak_release_year_global_sales=float(annual[y])),
        )
        for prefix, c in [("na", "NA_Sales"), ("eu", "EU_Sales"), ("jp", "JP_Sales")]:
            g = max(regions[c], key=regions[c].get)
            self.assertEqual(
                self.truth["answers"]["Q04_regions"][prefix + "_top_genre"], g
            )
            self.assertEqual(
                self.truth["answers"]["Q04_regions"][prefix + "_top_genre_sales"],
                float(regions[c][g]),
            )
        self.assertEqual(
            self.truth["answers"]["Q05_filtered"],
            dict(
                matching_rows=len(subset),
                global_sales_total=float(sum(d(r["Global_Sales"]) for r in subset)),
            ),
        )
        p = max(publishers, key=publishers.get)
        self.assertEqual(
            self.truth["answers"]["Q06_publishers"],
            dict(top_publisher=p, top_publisher_global_sales=float(publishers[p])),
        )

    def test_filter_null_and_any_semantics(self):
        t = DataTools(self.df, "unused")
        null = t.call(
            "query",
            query_args(filters=[dict(column="Year", operator="is_null", value=None)]),
        )
        self.assertEqual(null["rows"][0]["row_count"], 271)
        outside = t.call(
            "query",
            query_args(
                filters=[
                    dict(column="Year", operator="lt", value="1980"),
                    dict(column="Year", operator="gt", value="2016"),
                ],
                filter_mode="any",
            ),
        )
        self.assertEqual(outside["rows"][0]["row_count"], 4)
        bad = t.call(
            "query",
            query_args(filters=[dict(column="Revenue", operator="gt", value="0")]),
        )
        self.assertFalse(bad["ok"])
        self.assertNotIn("rows", bad)

    def test_controlled_failure_happens_once(self):
        t = DataTools(self.df, "unused", inject_failure=True)
        self.assertTrue(t.call("profile", {})["ok"])
        self.assertFalse(t.call("query", query_args())["ok"])
        self.assertTrue(t.call("query", query_args())["ok"])
        self.assertEqual(sum(c["injected"] for c in t.calls), 1)

    def test_evidence_validator_rejects_wrong_or_echoed_values(self):
        t = DataTools(self.df, "unused")
        t.call("query", query_args())
        self.assertEqual(
            verify_answer(claim_answer("16598"), t.receipts, ["matching_rows"], False),
            [],
        )
        self.assertTrue(
            verify_answer(claim_answer("16599"), t.receipts, ["matching_rows"], False)
        )
        self.assertTrue(
            verify_answer(
                claim_answer("50", pointer="/query/limit"),
                t.receipts,
                ["matching_rows"],
                False,
            )
        )
        self.assertTrue(
            verify_answer(
                claim_answer("16598", evidence="E999"),
                t.receipts,
                ["matching_rows"],
                False,
            )
        )

    def test_validator_does_not_use_answer_key(self):
        t = DataTools(self.df, "unused")
        t.call("query", query_args())
        # Receipt matching does not check whether a claim answers the question.
        answer = claim_answer("16598", field="net_profit_usd")
        self.assertEqual(
            verify_answer(answer, t.receipts, ["net_profit_usd"], False), []
        )

    def test_unsupported_cannot_assert_and_duplicates_fail(self):
        a = claim_answer("1")
        a["status"] = "unsupported"
        self.assertTrue(verify_answer(a, {}, ["matching_rows"], False))
        a = claim_answer(None)
        a["status"] = "unsupported"
        self.assertEqual(verify_answer(a, {}, ["matching_rows"], False), [])
        a["claims"] *= 2
        self.assertTrue(verify_answer(a, {}, ["matching_rows"], False))

    def test_plan_is_complete_balanced_and_unique(self):
        plan = planned_runs()
        self.assertEqual(len(plan), 198)
        self.assertEqual(len({p["run_id"] for p in plan}), 198)
        main = [p for p in plan if p["phase"] == "main"]
        for q in QUESTION_BY_ID:
            for c in CONDITIONS:
                self.assertEqual(
                    {
                        p["replication"]
                        for p in main
                        if p["condition"] == c and p["question_id"] == q
                    },
                    set(range(1, 6)),
                )
        for start in range(0, len(main), 3):
            self.assertEqual(
                {p["condition"] for p in main[start : start + 3]}, set(CONDITIONS)
            )
            self.assertEqual(
                len({p["question_id"] for p in main[start : start + 3]}), 1
            )

    def test_chart_data_and_artifact_verified(self):
        with tempfile.TemporaryDirectory() as tmp:
            t = DataTools(self.df, tmp)
            a = query_args(
                operation="aggregate",
                columns=["Global_Sales"],
                group_by=["Year"],
                filters=[dict(column="Year", operator="not_null", value=None)],
                sort_by=["Year"],
            )
            receipt = t.call("query", a)
            chart = t.call(
                "plot",
                dict(
                    evidence_id=receipt["evidence_id"],
                    kind="line",
                    x="Year",
                    ys=["Global_Sales"],
                    title="Recorded sales by release year",
                ),
            )
            self.assertTrue(chart["ok"], chart)
            self.assertTrue(
                chart_matches(chart, self.truth["plots"]["Q03_release_year"])
            )
            chart["rows"][0]["Global_Sales"] += 1
            self.assertFalse(
                chart_matches(chart, self.truth["plots"]["Q03_release_year"])
            )

    def test_wilson_boundaries(self):
        self.assertEqual(wilson(0, 0), (None, None))
        self.assertAlmostEqual(wilson(0, 30)[0], 0)
        self.assertAlmostEqual(wilson(30, 30)[1], 1)
        with self.assertRaises(ValueError):
            wilson(31, 30)

    def test_numeric_units_and_nonfinite(self):
        self.assertTrue(scalar_equal("678.90", 678.9))
        self.assertFalse(scalar_equal("678900000", 678.9))
        self.assertFalse(scalar_equal("NaN", 1))
        self.assertFalse(scalar_equal(True, 1))

    def test_budget_blocks_before_request(self):
        with tempfile.TemporaryDirectory() as tmp:
            client = Client("not-a-real-key", Path(tmp) / "ledger", limit=0.000001)
            with patch("urllib.request.urlopen") as call:
                with self.assertRaises(BudgetExceeded):
                    client.create({"max_output_tokens": 100}, "test")
                call.assert_not_called()

    def test_uncertain_cost_reservation_survives_restart(self):
        import urllib.error

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ledger"
            client = Client("not-a-real-key", path)
            payload = {"max_output_tokens": 100}
            with patch(
                "urllib.request.urlopen", side_effect=urllib.error.URLError("offline")
            ):
                with self.assertRaises(APIError):
                    client.create(payload, "test")
            restarted = Client("not-a-real-key", path)
            self.assertAlmostEqual(restarted.liability(), client.maximum_cost(payload))
            self.assertEqual(read_jsonl(path)[0]["event"], "reserved")


if __name__ == "__main__":
    unittest.main()
