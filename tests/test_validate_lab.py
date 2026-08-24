from __future__ import annotations

import csv
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "validate-lab.py"
SPEC = importlib.util.spec_from_file_location("validate_lab", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Cannot load validator from {MODULE_PATH}")
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class ValidateLabTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.submission = Path(self.temp_dir.name) / "submission"
        shutil.copytree(ROOT / "examples" / "hr-hiring", self.submission)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_complete_example_passes(self) -> None:
        self.assertEqual([], VALIDATOR.validate_submission_dir(self.submission))

    def test_template_fails_on_placeholders(self) -> None:
        errors = VALIDATOR.validate_submission_dir(ROOT / "templates")
        self.assertTrue(any("placeholder" in error for error in errors))
        self.assertTrue(any("must be an integer from 1 to 5" in error for error in errors))

    def test_unknown_harm_case_is_rejected(self) -> None:
        path = self.submission / "harm-map.csv"
        with path.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
            headers = list(rows[0])
        rows[0]["case_id"] = "CASE-99"
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)
        errors = VALIDATOR.validate_submission_dir(self.submission)
        self.assertTrue(any("unknown case 'CASE-99'" in error for error in errors))
        self.assertTrue(any("missing harm rows for cases: CASE-01" in error for error in errors))

    def test_unknown_case_source_is_rejected(self) -> None:
        path = self.submission / "case-studies.csv"
        with path.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
            headers = list(rows[0])
        rows[0]["source_ids"] = "SRC-99"
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)
        errors = VALIDATOR.validate_submission_dir(self.submission)
        self.assertTrue(any("unknown source IDs: SRC-99" in error for error in errors))

    def test_snapshot_score_outside_range_is_rejected(self) -> None:
        path = self.submission / "submission.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["industry_risk_snapshot"]["high_stakes"] = 6
        path.write_text(json.dumps(data), encoding="utf-8")
        errors = VALIDATOR.validate_submission_dir(self.submission)
        self.assertTrue(any("industry_risk_snapshot.high_stakes" in error for error in errors))

    def test_truncated_harm_row_reports_errors_instead_of_crashing(self) -> None:
        path = self.submission / "harm-map.csv"
        lines = path.read_text(encoding="utf-8").splitlines()
        first_row = lines[1].split(",")
        lines[1] = ",".join(first_row[:-3])
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        errors = VALIDATOR.validate_submission_dir(self.submission)
        self.assertTrue(any("monitoring_metric" in error for error in errors))
        self.assertTrue(any("response_action" in error for error in errors))

    def test_unknown_publication_date_is_allowed(self) -> None:
        path = self.submission / "sources.csv"
        with path.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
            headers = list(rows[0])
        rows[0]["published_at"] = "unknown"
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)
        self.assertEqual([], VALIDATOR.validate_submission_dir(self.submission))

    def test_missing_product_fallback_is_rejected(self) -> None:
        path = self.submission / "submission.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["product_context"]["fallback_experience"] = ""
        path.write_text(json.dumps(data), encoding="utf-8")
        errors = VALIDATOR.validate_submission_dir(self.submission)
        self.assertTrue(any("product_context.fallback_experience" in error for error in errors))

    def test_release_decision_must_trace_blocking_gap_ids(self) -> None:
        path = self.submission / "submission.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["release_decision"]["release_blockers"] = ["review still pending"]
        path.write_text(json.dumps(data), encoding="utf-8")
        errors = VALIDATOR.validate_submission_dir(self.submission)
        self.assertTrue(any("missing blocking gap IDs: GAP-01, GAP-02" in error for error in errors))

    def test_completed_blocking_gaps_allow_go_decision(self) -> None:
        gap_path = self.submission / "compliance-gap-analysis.csv"
        with gap_path.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
            headers = list(rows[0])
        for row in rows:
            if row["release_blocking"] == "yes":
                row["status"] = "done"
        with gap_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)

        submission_path = self.submission / "submission.json"
        data = json.loads(submission_path.read_text(encoding="utf-8"))
        data["release_decision"]["decision"] = "go"
        data["release_decision"]["release_blockers"] = ["none"]
        submission_path.write_text(json.dumps(data), encoding="utf-8")

        self.assertEqual([], VALIDATOR.validate_submission_dir(self.submission))

    def test_acceptance_criteria_must_use_given_when_then(self) -> None:
        path = self.submission / "compliance-gap-analysis.csv"
        with path.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
            headers = list(rows[0])
        rows[0]["acceptance_criteria"] = "The team should review this before launch"
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)
        errors = VALIDATOR.validate_submission_dir(self.submission)
        self.assertTrue(any("acceptance_criteria: use Given / When / Then" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
