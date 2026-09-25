"""Tests for post hoc review provenance and denominator/variance failures."""

from pathlib import Path
import copy, json, sys, unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from trace_review_analysis import validate_annotations, dispersion


class ReviewIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = (ROOT / "outputs/study_v1/runs.jsonl").read_bytes()
        cls.records = [json.loads(x) for x in cls.raw.splitlines()]
        cls.labels = json.loads(
            (ROOT / "config/trace_review_annotations.json").read_text()
        )
        cls.rubric = (ROOT / "documentation/TRACE_REVIEW_RUBRIC.md").read_bytes()

    def check(self, labels):
        return validate_annotations(self.records, labels, self.rubric, self.raw)

    def test_every_record_and_call_bound_to_source(self):
        reviewed = self.check(self.labels)
        self.assertEqual(len(reviewed), 198)
        self.assertEqual(sum(len(x["calls"]) for x in reviewed), 385)

    def test_missing_rating_is_not_silently_excluded(self):
        x = copy.deepcopy(self.labels)
        x["records"].pop()
        with self.assertRaisesRegex(ValueError, "coverage"):
            self.check(x)

    def test_changed_record_invalidates_rating(self):
        records = copy.deepcopy(self.records)
        records[0]["answer"]["explanation"] += " edited"
        with self.assertRaisesRegex(ValueError, "source record"):
            validate_annotations(records, self.labels, self.rubric, self.raw)

    def test_injected_failure_cannot_enter_ordinary_denominator(self):
        x = copy.deepcopy(self.labels)
        c = next(c for r in x["records"] for c in r["calls"] if c["injected"])
        c["eligible_selection"] = True
        with self.assertRaisesRegex(ValueError, "eligibility"):
            self.check(x)

    def test_profile_does_not_get_free_parameter_credit(self):
        x = copy.deepcopy(self.labels)
        c = next(c for r in x["records"] for c in r["calls"] if c["tool"] == "profile")
        c["eligible_parameters"] = True
        with self.assertRaisesRegex(ValueError, "eligibility"):
            self.check(x)

    def test_nulls_are_not_zero_and_single_value_has_no_variance(self):
        d = dispersion([None, 678.9, None])
        self.assertEqual(d["n"], 1)
        self.assertIsNone(d["sample_variance"])
        self.assertEqual(dispersion([0, 0, 1, 1, 1])["sample_variance"], 0.3)
        self.assertIsNone(dispersion([])["mean"])


if __name__ == "__main__":
    unittest.main()
