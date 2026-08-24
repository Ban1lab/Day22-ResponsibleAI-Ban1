#!/usr/bin/env python3
"""Validate a Responsible AI lab submission using only the Python standard library."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "lab.config.json"
REQUIRED_FILES = (
    "submission.json",
    "sources.csv",
    "case-studies.csv",
    "harm-map.csv",
    "compliance-gap-analysis.csv",
    "group-synthesis.csv",
)
PLACEHOLDER_RE = re.compile(r"<[^>]+>|\b(?:TODO|TBD)\b|example\.invalid", re.IGNORECASE)
SOURCE_ID_RE = re.compile(r"^SRC-\d{2,}$")
CASE_ID_RE = re.compile(r"^CASE-\d{2,}$")
GAP_ID_RE = re.compile(r"^GAP-\d{2,}$")

SOURCE_HEADERS = (
    "source_id",
    "title",
    "publisher",
    "published_at",
    "accessed_at",
    "url",
    "authority_level",
    "supports_claim",
    "limitations",
)
CASE_HEADERS = (
    "case_id",
    "title",
    "year",
    "industry",
    "system_purpose",
    "decision_impact",
    "affected_groups",
    "verified_facts",
    "reported_harm",
    "quantitative_evidence",
    "source_ids",
    "limitations",
)
HARM_HEADERS = (
    "case_id",
    "high_risk_moment",
    "stakeholder",
    "stakeholder_type",
    "failure_mode",
    "failure_layer",
    "harm_lens",
    "harm_description",
    "severity_1_5",
    "likelihood_1_5",
    "scale_1_5",
    "frequency_1_5",
    "evidence_source_ids",
    "existing_controls",
    "proposed_controls",
    "human_oversight",
    "residual_severity_1_5",
    "residual_likelihood_1_5",
    "owner",
    "monitoring_metric",
    "trigger_threshold",
    "response_action",
)
GAP_HEADERS = (
    "gap_id",
    "jurisdiction",
    "product_risk_or_requirement",
    "current_state",
    "product_requirement",
    "acceptance_criteria",
    "priority",
    "release_blocking",
    "owner",
    "target_milestone",
    "deadline_or_trigger",
    "status",
    "evidence_needed",
    "source_ids",
)
GROUP_HEADERS = (
    "group_id",
    "industries_compared",
    "highest_stakes_industry",
    "recurring_harms",
    "common_failure_layers",
    "human_in_loop_decisions",
    "strongest_guardrails",
    "cross_industry_pattern",
    "evidence_source_ids",
)


def load_json(path: Path, errors: list[str]) -> dict[str, Any]:
    try:
        with path.open(encoding="utf-8") as handle:
            value = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path.name}: cannot read valid JSON: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{path.name}: top-level value must be an object")
        return {}
    return value


def load_csv(path: Path, expected_headers: tuple[str, ...], errors: list[str]) -> list[dict[str, str]]:
    try:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            headers = tuple(reader.fieldnames or ())
            missing = [header for header in expected_headers if header not in headers]
            if missing:
                errors.append(f"{path.name}: missing columns: {', '.join(missing)}")
            return [dict(row) for row in reader]
    except (OSError, csv.Error) as exc:
        errors.append(f"{path.name}: cannot read valid CSV: {exc}")
        return []


def cell(row: dict[str, str], field: str) -> str:
    value = row.get(field, "")
    return value.strip() if isinstance(value, str) else ""


def split_ids(raw: Any) -> list[str]:
    if not isinstance(raw, str):
        return []
    return [item.strip() for item in raw.split(";") if item.strip()]


def is_placeholder(value: Any) -> bool:
    if isinstance(value, str):
        return bool(PLACEHOLDER_RE.search(value))
    if isinstance(value, dict):
        return any(is_placeholder(item) for item in value.values())
    if isinstance(value, list):
        return any(is_placeholder(item) for item in value)
    return False


def require_text(value: Any, field: str, errors: list[str], minimum: int = 2) -> None:
    if not isinstance(value, str) or len(value.strip()) < minimum:
        errors.append(f"{field}: must contain at least {minimum} characters")
    elif is_placeholder(value):
        errors.append(f"{field}: replace placeholder text")


def require_string_list(value: Any, field: str, errors: list[str]) -> None:
    if not isinstance(value, list) or not value:
        errors.append(f"{field}: must be a non-empty list")
        return
    for index, item in enumerate(value):
        require_text(item, f"{field}[{index}]", errors, 1)


def require_score(value: Any, field: str, config: dict[str, Any], errors: list[str]) -> None:
    minimum = config["score_min"]
    maximum = config["score_max"]
    if not isinstance(value, int) or isinstance(value, bool) or not minimum <= value <= maximum:
        errors.append(f"{field}: must be an integer from {minimum} to {maximum}")


def require_date(value: str, field: str, errors: list[str]) -> None:
    try:
        date.fromisoformat(value)
    except (TypeError, ValueError):
        errors.append(f"{field}: must be an ISO-8601 date (YYYY-MM-DD)")


def require_publication_date(value: Any, field: str, errors: list[str]) -> None:
    if isinstance(value, str) and value.strip().lower() == "unknown":
        return
    require_date(value, field, errors)


def validate_source_refs(raw: str, field: str, source_ids: set[str], errors: list[str]) -> None:
    references = split_ids(raw)
    if not references:
        errors.append(f"{field}: cite at least one source ID")
        return
    unknown = [source_id for source_id in references if source_id not in source_ids]
    if unknown:
        errors.append(f"{field}: unknown source IDs: {', '.join(unknown)}")


def validate_sources(rows: list[dict[str, str]], config: dict[str, Any], errors: list[str]) -> set[str]:
    source_ids: set[str] = set()
    primary_count = 0
    if len(rows) < 2:
        errors.append("sources.csv: include at least two sources")
    for index, row in enumerate(rows, start=2):
        prefix = f"sources.csv:{index}"
        source_id = cell(row, "source_id")
        if not SOURCE_ID_RE.fullmatch(source_id):
            errors.append(f"{prefix}.source_id: use SRC-01 style")
        elif source_id in source_ids:
            errors.append(f"{prefix}.source_id: duplicate {source_id}")
        else:
            source_ids.add(source_id)

        for field, minimum in (
            ("title", 5),
            ("publisher", 2),
            ("supports_claim", 20),
            ("limitations", 10),
        ):
            require_text(row.get(field), f"{prefix}.{field}", errors, minimum)
        require_publication_date(row.get("published_at", ""), f"{prefix}.published_at", errors)
        require_date(row.get("accessed_at", ""), f"{prefix}.accessed_at", errors)

        url = cell(row, "url")
        parsed = urlparse(url)
        if parsed.scheme != "https" or not parsed.netloc or is_placeholder(url):
            errors.append(f"{prefix}.url: use a non-placeholder HTTPS source URL")

        authority = cell(row, "authority_level")
        if authority not in config["source_authority_levels"]:
            errors.append(f"{prefix}.authority_level: invalid value {authority!r}")
        if authority in {"primary-official", "primary-peer-reviewed"}:
            primary_count += 1
    if rows and primary_count == 0:
        errors.append("sources.csv: include at least one primary official or peer-reviewed source")
    return source_ids


def validate_submission(
    data: dict[str, Any], config: dict[str, Any], source_ids: set[str], errors: list[str]
) -> str:
    if data.get("schema_version") != config["schema_version"]:
        errors.append(f"submission.json.schema_version: expected {config['schema_version']}")
    if is_placeholder(data):
        errors.append("submission.json: replace all placeholder text")

    metadata = data.get("metadata")
    if not isinstance(metadata, dict):
        errors.append("submission.json.metadata: must be an object")
    else:
        for field in ("student_name", "student_id", "group_id"):
            require_text(metadata.get(field), f"submission.json.metadata.{field}", errors)
        submitted_at = metadata.get("submitted_at")
        try:
            datetime.fromisoformat(submitted_at)
        except (TypeError, ValueError):
            errors.append("submission.json.metadata.submitted_at: must be an ISO-8601 date-time")

    industry = data.get("industry", "")
    if industry not in config["industries"]:
        errors.append(f"submission.json.industry: invalid value {industry!r}")

    product = data.get("product_context")
    if not isinstance(product, dict):
        errors.append("submission.json.product_context: must be an object")
    else:
        for field, minimum in (
            ("product_name", 2),
            ("problem_statement", 20),
            ("value_hypothesis", 20),
            ("user_journey_moment", 10),
            ("fallback_experience", 20),
        ):
            require_text(product.get(field), f"submission.json.product_context.{field}", errors, minimum)
        for field in ("target_users", "in_scope", "non_goals"):
            require_string_list(product.get(field), f"submission.json.product_context.{field}", errors)
        product_stage = product.get("product_stage")
        if product_stage not in config["product_stages"]:
            errors.append(f"submission.json.product_context.product_stage: invalid value {product_stage!r}")
        automation_level = product.get("automation_level")
        if automation_level not in config["automation_levels"]:
            errors.append(
                f"submission.json.product_context.automation_level: invalid value {automation_level!r}"
            )
        reversibility = product.get("decision_reversibility")
        if reversibility not in config["decision_reversibility_levels"]:
            errors.append(
                f"submission.json.product_context.decision_reversibility: invalid value {reversibility!r}"
            )
        require_date(
            product.get("target_launch_or_review_date", ""),
            "submission.json.product_context.target_launch_or_review_date",
            errors,
        )

    profile = data.get("system_profile")
    if not isinstance(profile, dict):
        errors.append("submission.json.system_profile: must be an object")
    else:
        for field, minimum in (
            ("purpose", 20),
            ("decision_impact", 20),
            ("deployment_context", 20),
        ):
            require_text(profile.get(field), f"submission.json.system_profile.{field}", errors, minimum)
        for field in ("user_groups", "data_types", "target_markets"):
            require_string_list(profile.get(field), f"submission.json.system_profile.{field}", errors)
        boundary = profile.get("system_boundary")
        if not isinstance(boundary, dict):
            errors.append("submission.json.system_profile.system_boundary: must be an object")
        else:
            for field in ("model", "application"):
                require_text(
                    boundary.get(field),
                    f"submission.json.system_profile.system_boundary.{field}",
                    errors,
                )
            for field in ("people", "vendors", "upstream_inputs", "downstream_decisions"):
                require_string_list(
                    boundary.get(field),
                    f"submission.json.system_profile.system_boundary.{field}",
                    errors,
                )

    snapshot = data.get("industry_risk_snapshot")
    if not isinstance(snapshot, dict):
        errors.append("submission.json.industry_risk_snapshot: must be an object")
    else:
        for metric in config["risk_metrics"]:
            require_score(
                snapshot.get(metric),
                f"submission.json.industry_risk_snapshot.{metric}",
                config,
                errors,
            )
        require_text(
            snapshot.get("rationale"),
            "submission.json.industry_risk_snapshot.rationale",
            errors,
            80,
        )

    classification = data.get("legal_classification")
    if not isinstance(classification, dict):
        errors.append("submission.json.legal_classification: must be an object")
    else:
        for jurisdiction in ("vietnam", "eu"):
            assessment = classification.get(jurisdiction)
            prefix = f"submission.json.legal_classification.{jurisdiction}"
            if not isinstance(assessment, dict):
                errors.append(f"{prefix}: must be an object")
                continue
            status = assessment.get("status")
            if status not in config["legal_classification_statuses"]:
                errors.append(f"{prefix}.status: invalid value {status!r}")
            require_text(assessment.get("rationale"), f"{prefix}.rationale", errors, 40)
            refs = assessment.get("source_ids")
            if not isinstance(refs, list) or not refs:
                errors.append(f"{prefix}.source_ids: must be a non-empty list")
            else:
                unknown = [source_id for source_id in refs if source_id not in source_ids]
                if unknown:
                    errors.append(f"{prefix}.source_ids: unknown source IDs: {', '.join(unknown)}")
        require_text(
            classification.get("other_markets"),
            "submission.json.legal_classification.other_markets",
            errors,
            10,
        )
        if not isinstance(classification.get("legal_review_required"), bool):
            errors.append("submission.json.legal_classification.legal_review_required: must be boolean")

    metrics = data.get("product_metrics")
    if not isinstance(metrics, dict):
        errors.append("submission.json.product_metrics: must be an object")
    else:
        for field, minimum in (
            ("success_kpi", 20),
            ("risk_kri", 20),
            ("guardrail_metric", 20),
            ("review_cadence", 10),
        ):
            require_text(metrics.get(field), f"submission.json.product_metrics.{field}", errors, minimum)

    release = data.get("release_decision")
    if not isinstance(release, dict):
        errors.append("submission.json.release_decision: must be an object")
    else:
        for field in ("accountable_product_owner", "risk_acceptance_owner", "independent_reviewer"):
            require_text(release.get(field), f"submission.json.release_decision.{field}", errors)
        if release.get("decision") not in {"go", "conditional-go", "no-go", "research-only"}:
            errors.append("submission.json.release_decision.decision: invalid value")
        for field in ("release_blockers", "release_conditions"):
            require_string_list(release.get(field), f"submission.json.release_decision.{field}", errors)
        require_text(
            release.get("next_review_trigger"),
            "submission.json.release_decision.next_review_trigger",
            errors,
            20,
        )
        require_text(
            release.get("residual_risk_rationale"),
            "submission.json.release_decision.residual_risk_rationale",
            errors,
            40,
        )
    return industry


def validate_cases(
    rows: list[dict[str, str]], industry: str, source_ids: set[str], config: dict[str, Any], errors: list[str]
) -> set[str]:
    case_ids: set[str] = set()
    minimum = config["case_count_min"]
    maximum = config["case_count_max"]
    if not minimum <= len(rows) <= maximum:
        errors.append(f"case-studies.csv: include {minimum} to {maximum} cases; found {len(rows)}")
    for index, row in enumerate(rows, start=2):
        prefix = f"case-studies.csv:{index}"
        case_id = cell(row, "case_id")
        if not CASE_ID_RE.fullmatch(case_id):
            errors.append(f"{prefix}.case_id: use CASE-01 style")
        elif case_id in case_ids:
            errors.append(f"{prefix}.case_id: duplicate {case_id}")
        else:
            case_ids.add(case_id)
        for field, minimum_length in (
            ("title", 5),
            ("system_purpose", 10),
            ("decision_impact", 10),
            ("affected_groups", 3),
            ("verified_facts", 20),
            ("reported_harm", 10),
            ("quantitative_evidence", 15),
            ("limitations", 15),
        ):
            require_text(row.get(field), f"{prefix}.{field}", errors, minimum_length)
        try:
            year = int(cell(row, "year"))
            if not 2000 <= year <= date.today().year + 1:
                raise ValueError
        except (TypeError, ValueError):
            errors.append(f"{prefix}.year: use a plausible four-digit year")
        if row.get("industry") != industry:
            errors.append(f"{prefix}.industry: must match submission.json industry {industry!r}")
        validate_source_refs(row.get("source_ids", ""), f"{prefix}.source_ids", source_ids, errors)
    return case_ids


def validate_harms(
    rows: list[dict[str, str]], case_ids: set[str], source_ids: set[str], config: dict[str, Any], errors: list[str]
) -> None:
    covered_cases: set[str] = set()
    has_non_customer = False
    if not rows:
        errors.append("harm-map.csv: include at least one harm row per case")
    score_fields = (
        "severity_1_5",
        "likelihood_1_5",
        "scale_1_5",
        "frequency_1_5",
        "residual_severity_1_5",
        "residual_likelihood_1_5",
    )
    text_fields = (
        "high_risk_moment",
        "stakeholder",
        "harm_description",
        "existing_controls",
        "proposed_controls",
        "human_oversight",
        "owner",
        "monitoring_metric",
        "trigger_threshold",
        "response_action",
    )
    for index, row in enumerate(rows, start=2):
        prefix = f"harm-map.csv:{index}"
        case_id = cell(row, "case_id")
        if case_id not in case_ids:
            errors.append(f"{prefix}.case_id: unknown case {case_id!r}")
        else:
            covered_cases.add(case_id)
        for field in text_fields:
            require_text(row.get(field), f"{prefix}.{field}", errors, 2)
        stakeholder_type = cell(row, "stakeholder_type")
        if stakeholder_type not in config["stakeholder_types"]:
            errors.append(f"{prefix}.stakeholder_type: invalid value {stakeholder_type!r}")
        if stakeholder_type == "affected-non-customer":
            has_non_customer = True
        for field, config_key in (
            ("failure_mode", "failure_modes"),
            ("failure_layer", "failure_layers"),
            ("harm_lens", "harm_lenses"),
        ):
            value = cell(row, field)
            if value not in config[config_key]:
                errors.append(f"{prefix}.{field}: invalid value {value!r}")
        for field in score_fields:
            try:
                value = int(cell(row, field))
            except (TypeError, ValueError):
                value = None
            require_score(value, f"{prefix}.{field}", config, errors)
        validate_source_refs(
            row.get("evidence_source_ids", ""),
            f"{prefix}.evidence_source_ids",
            source_ids,
            errors,
        )
    missing_cases = sorted(case_ids - covered_cases)
    if missing_cases:
        errors.append(f"harm-map.csv: missing harm rows for cases: {', '.join(missing_cases)}")
    if rows and not has_non_customer:
        errors.append("harm-map.csv: include at least one affected-non-customer stakeholder")


def validate_gaps(
    rows: list[dict[str, str]], source_ids: set[str], config: dict[str, Any], errors: list[str]
) -> set[str]:
    gap_ids: set[str] = set()
    blocking_gap_ids: set[str] = set()
    if not rows:
        errors.append("compliance-gap-analysis.csv: include at least one gap or not-applicable assessment")
    for index, row in enumerate(rows, start=2):
        prefix = f"compliance-gap-analysis.csv:{index}"
        gap_id = cell(row, "gap_id")
        if not GAP_ID_RE.fullmatch(gap_id):
            errors.append(f"{prefix}.gap_id: use GAP-01 style")
        elif gap_id in gap_ids:
            errors.append(f"{prefix}.gap_id: duplicate {gap_id}")
        else:
            gap_ids.add(gap_id)
        for field in (
            "jurisdiction",
            "product_risk_or_requirement",
            "current_state",
            "product_requirement",
            "acceptance_criteria",
            "owner",
            "target_milestone",
            "deadline_or_trigger",
            "evidence_needed",
        ):
            require_text(row.get(field), f"{prefix}.{field}", errors, 2)
        acceptance = cell(row, "acceptance_criteria").lower()
        if not all(keyword in acceptance for keyword in ("given", "when", "then")):
            errors.append(f"{prefix}.acceptance_criteria: use Given / When / Then")
        priority = cell(row, "priority")
        if priority not in config["backlog_priorities"]:
            errors.append(f"{prefix}.priority: invalid value {priority!r}")
        status = cell(row, "status")
        if status not in config["action_statuses"]:
            errors.append(f"{prefix}.status: invalid value {status!r}")
        release_blocking = cell(row, "release_blocking")
        if release_blocking not in config["release_blocking_values"]:
            errors.append(f"{prefix}.release_blocking: use yes or no")
        elif release_blocking == "yes" and status != "done" and GAP_ID_RE.fullmatch(gap_id):
            blocking_gap_ids.add(gap_id)
        validate_source_refs(row.get("source_ids", ""), f"{prefix}.source_ids", source_ids, errors)
    return blocking_gap_ids


def validate_release_traceability(
    submission: dict[str, Any], blocking_gap_ids: set[str], errors: list[str]
) -> None:
    release = submission.get("release_decision")
    if not isinstance(release, dict):
        return
    decision = release.get("decision")
    blockers = release.get("release_blockers")
    blocker_text = (
        " ".join(item for item in blockers if isinstance(item, str))
        if isinstance(blockers, list)
        else ""
    )
    missing = [gap_id for gap_id in sorted(blocking_gap_ids) if gap_id not in blocker_text]
    if missing:
        errors.append(
            "submission.json.release_decision.release_blockers: missing blocking gap IDs: "
            + ", ".join(missing)
        )
    if decision == "go" and blocking_gap_ids:
        errors.append("submission.json.release_decision.decision: cannot be go with open release-blocking gaps")


def validate_group(rows: list[dict[str, str]], source_ids: set[str], errors: list[str]) -> None:
    if not rows:
        errors.append("group-synthesis.csv: include one group synthesis row")
        return
    if len(rows) > 1:
        errors.append(f"group-synthesis.csv: expected one synthesis row; found {len(rows)}")
    for index, row in enumerate(rows, start=2):
        prefix = f"group-synthesis.csv:{index}"
        for field in GROUP_HEADERS[:-1]:
            require_text(row.get(field), f"{prefix}.{field}", errors, 2)
        validate_source_refs(
            row.get("evidence_source_ids", ""),
            f"{prefix}.evidence_source_ids",
            source_ids,
            errors,
        )


def validate_submission_dir(submission_dir: Path) -> list[str]:
    errors: list[str] = []
    if not submission_dir.is_dir():
        return [f"submission directory not found: {submission_dir}"]
    missing_files = [name for name in REQUIRED_FILES if not (submission_dir / name).is_file()]
    if missing_files:
        errors.append(f"missing required files: {', '.join(missing_files)}")
        return errors

    config = load_json(CONFIG_PATH, errors)
    if not config:
        return errors
    submission = load_json(submission_dir / "submission.json", errors)
    source_rows = load_csv(submission_dir / "sources.csv", SOURCE_HEADERS, errors)
    case_rows = load_csv(submission_dir / "case-studies.csv", CASE_HEADERS, errors)
    harm_rows = load_csv(submission_dir / "harm-map.csv", HARM_HEADERS, errors)
    gap_rows = load_csv(submission_dir / "compliance-gap-analysis.csv", GAP_HEADERS, errors)
    group_rows = load_csv(submission_dir / "group-synthesis.csv", GROUP_HEADERS, errors)

    source_ids = validate_sources(source_rows, config, errors)
    industry = validate_submission(submission, config, source_ids, errors)
    case_ids = validate_cases(case_rows, industry, source_ids, config, errors)
    validate_harms(harm_rows, case_ids, source_ids, config, errors)
    blocking_gap_ids = validate_gaps(gap_rows, source_ids, config, errors)
    validate_release_traceability(submission, blocking_gap_ids, errors)
    validate_group(group_rows, source_ids, errors)
    return errors


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("submission_dir", type=Path, help="directory containing the six submission files")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    errors = validate_submission_dir(args.submission_dir.resolve())
    if errors:
        print(f"FAIL: {len(errors)} validation error(s)")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"PASS: {args.submission_dir} is structurally complete")
    print("NOTE: structural validation is not fact-checking, legal advice, or compliance certification")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
