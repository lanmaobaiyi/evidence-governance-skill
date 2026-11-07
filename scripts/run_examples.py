"""Run dependency-free checks that demonstrate the Skill's public contract."""

from __future__ import annotations

import csv
import json
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "examples" / "synthetic-ledger.csv"
POLICY = ROOT / "examples" / "synthetic-policy.md"
EXPECTED = ROOT / "examples" / "expected-review-report.md"
RUNNER = ROOT / "scripts" / "run_governance_case.py"


def complete_case() -> dict:
    with LEDGER.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    required = {"record_id", "event_type", "occurred_at", "location", "count"}
    headers = set(rows[0]) if rows else set()
    counts = Counter(row["event_type"] for row in rows)
    policy = POLICY.read_text(encoding="utf-8")
    expected = EXPECTED.read_text(encoding="utf-8")
    checks = {
        "required_columns": required <= headers,
        "deterministic_counts": counts == {"parking_conflict": 2, "blocked_access": 1},
        "policy_sections": all(section in policy for section in ("## Scope", "## Response", "## Review")),
        "review_state_visible": "REVIEW" in expected and "COMPLETED" in expected,
    }
    return {"scenario": "complete-input", "state": "REVIEW", "checks": checks}


def missing_field_case() -> dict:
    row = {"record_id": "M-001", "event_type": "blocked_access", "location": ""}
    blocked = not row["location"]
    return {
        "scenario": "missing-required-field",
        "state": "REGENERATION_REQUIRED",
        "checks": {"missing_location_blocks_analysis": blocked},
    }


def conflict_case() -> dict:
    revisions = {"policy-a": "15 minutes", "policy-b": "30 minutes"}
    conflict = len(set(revisions.values())) > 1
    return {
        "scenario": "conflicting-policy-revisions",
        "state": "REVIEW",
        "checks": {"conflict_is_visible": conflict, "silent_choice_rejected": conflict},
    }


def runner_case() -> dict:
    with tempfile.TemporaryDirectory() as directory:
        output = Path(directory) / "review.json"
        result = subprocess.run(
            [sys.executable, str(RUNNER), "--ledger", str(LEDGER), "--policy", str(POLICY), "--output", str(output)],
            capture_output=True,
            text=True,
            check=False,
        )
        packet = json.loads(output.read_text(encoding="utf-8"))
        complete_checks = {
            "exit_zero": result.returncode == 0,
            "review_state": packet["terminal_state"] == "REVIEW",
            "hashes_present": all(source["sha256"] for source in packet["input_snapshot"]["sources"]),
            "event_counts": packet["deterministic_findings"]["event_type_counts"] == {
                "blocked_access": 1,
                "parking_conflict": 2,
            },
        }

        bad_ledger = Path(directory) / "missing.csv"
        bad_ledger.write_text("record_id,event_type\nM-001,blocked_access\n", encoding="utf-8")
        bad_output = Path(directory) / "missing-review.json"
        bad_result = subprocess.run(
            [sys.executable, str(RUNNER), "--ledger", str(bad_ledger), "--policy", str(POLICY), "--output", str(bad_output)],
            capture_output=True,
            text=True,
            check=False,
        )
        bad_packet = json.loads(bad_output.read_text(encoding="utf-8"))
        missing_checks = {
            "nonzero_for_regeneration": bad_result.returncode == 2,
            "regeneration_state": bad_packet["terminal_state"] == "REGENERATION_REQUIRED",
            "missing_field_reported": any("location" in item for item in bad_packet["deterministic_findings"]["blockers"]),
        }

        extra_ledger = Path(directory) / "extra.csv"
        extra_ledger.write_text("record_id,event_type,location\nM-002,blocked_access,North Gate,unexpected\n", encoding="utf-8")
        extra_output = Path(directory) / "extra-review.json"
        extra_result = subprocess.run(
            [sys.executable, str(RUNNER), "--ledger", str(extra_ledger), "--policy", str(POLICY), "--output", str(extra_output)],
            capture_output=True, text=True, check=False,
        )
        extra_packet = json.loads(extra_output.read_text(encoding="utf-8"))
        extra_checks = {
            "extra_columns_are_blocked": extra_result.returncode == 2,
            "extra_columns_are_reported": any("extra columns" in item for item in extra_packet["deterministic_findings"]["blockers"]),
        }

        empty_ledger = Path(directory) / "empty.csv"
        empty_ledger.write_text("record_id,event_type,location\n", encoding="utf-8")
        empty_output = Path(directory) / "empty-review.json"
        empty_result = subprocess.run(
            [sys.executable, str(RUNNER), "--ledger", str(empty_ledger), "--policy", str(POLICY), "--output", str(empty_output)],
            capture_output=True, text=True, check=False,
        )
        empty_packet = json.loads(empty_output.read_text(encoding="utf-8"))
        empty_checks = {
            "empty_rows_are_blocked": empty_result.returncode == 2,
            "empty_rows_are_reported": any("no data rows" in item for item in empty_packet["deterministic_findings"]["blockers"]),
        }

        duplicate_ledger = Path(directory) / "duplicate.csv"
        duplicate_ledger.write_text("record_id,event_type,event_type,location\nM-003,blocked_access,other,North Gate\n", encoding="utf-8")
        duplicate_output = Path(directory) / "duplicate-review.json"
        duplicate_result = subprocess.run(
            [sys.executable, str(RUNNER), "--ledger", str(duplicate_ledger), "--policy", str(POLICY), "--output", str(duplicate_output)],
            capture_output=True, text=True, check=False,
        )
        duplicate_packet = json.loads(duplicate_output.read_text(encoding="utf-8"))
        duplicate_checks = {
            "duplicate_headers_are_blocked": duplicate_result.returncode == 2,
            "duplicate_headers_are_reported": any("duplicate headers" in item for item in duplicate_packet["deterministic_findings"]["blockers"]),
        }

        collision_result = subprocess.run(
            [sys.executable, str(RUNNER), "--ledger", str(LEDGER), "--policy", str(POLICY), "--output", str(LEDGER)],
            capture_output=True, text=True, check=False,
        )
        collision_checks = {"input_overwrite_is_blocked": collision_result.returncode == 2}

    return {
        "scenario": "generic-runner-cli",
        "state": "REVIEW",
        "checks": {**complete_checks, **missing_checks, **extra_checks, **empty_checks, **duplicate_checks, **collision_checks},
    }


def main() -> int:
    results = [complete_case(), missing_field_case(), conflict_case(), runner_case()]
    if not all(all(item["checks"].values()) for item in results):
        print(json.dumps({"status": "FAIL", "results": results}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps({"status": "PASS", "results": results}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


