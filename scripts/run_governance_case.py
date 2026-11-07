"""Run a dependency-free, deterministic governance review over CSV + Markdown.

This script creates a review packet. It does not call a model, network, database,
or external service, and it never performs a governance action.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

RUNNER_VERSION = "0.2.0"
REQUIRED_FIELDS = ("event_type", "location")
RECOMMENDED_FIELDS = ("record_id", "occurred_at", "count")


def clean_cell(value: object) -> str:
    if isinstance(value, list):
        return ",".join(str(item).strip() for item in value)
    return str(value or "").strip()


def sha256_file(path: Path) -> str | None:
    if not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def source_snapshot(path: Path, role: str) -> dict[str, Any]:
    return {"role": role, "path": path.name, "exists": path.is_file(), "sha256": sha256_file(path)}


def read_ledger(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]], list[str]]:
    errors: list[str] = []
    if not path.is_file():
        return {"headers": [], "row_count": 0}, [], [f"ledger file not found: {path}"]
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle, restkey="__extra__")
            headers = [header.strip() for header in (reader.fieldnames or []) if header]
            rows: list[dict[str, str]] = []
            for index, raw_row in enumerate(reader, start=2):
                extras = raw_row.pop("__extra__", None)
                if extras:
                    errors.append(f"ledger row {index} has extra columns")
                row = {
                    (key or "").strip(): clean_cell(value)
                    for key, value in raw_row.items()
                    if key is not None
                }
                rows.append(row)
    except (OSError, UnicodeError, csv.Error) as exc:
        return {"headers": [], "row_count": 0}, [], [f"ledger could not be parsed: {exc}"]
    if not headers:
        errors.append("ledger has no header row")
    missing = sorted(set(REQUIRED_FIELDS) - set(headers))
    if missing:
        errors.append("ledger is missing required fields: " + ", ".join(missing))
    if not rows:
        errors.append("ledger has no data rows")
    normalized = [header.casefold() for header in headers]
    duplicates = sorted({header for header in normalized if normalized.count(header) > 1})
    if duplicates:
        errors.append("ledger has duplicate headers: " + ", ".join(duplicates))
    for index, row in enumerate(rows, start=2):
        for field in REQUIRED_FIELDS:
            if field in headers and not row.get(field, ""):
                errors.append(f"ledger row {index} has an empty required field: {field}")
    return {
        "headers": headers,
        "row_count": len(rows),
        "missing_recommended_fields": sorted(set(RECOMMENDED_FIELDS) - set(headers)),
    }, rows, errors


def read_policy(path: Path) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    if not path.is_file():
        return {"headings": [], "line_count": 0}, [f"policy file not found: {path}"]
    try:
        text = path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as exc:
        return {"headings": [], "line_count": 0}, [f"policy could not be read: {exc}"]
    if not text.strip():
        errors.append("policy is empty")
    headings = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        match = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
        if match:
            headings.append({"title": match.group(1), "line": line_number})
    if not headings:
        errors.append("policy has no Markdown heading to cite")
    return {"headings": headings, "line_count": len(text.splitlines())}, errors


def build_packet(ledger_path: Path, policy_path: Path) -> dict[str, Any]:
    ledger, rows, ledger_errors = read_ledger(ledger_path)
    policy, policy_errors = read_policy(policy_path)
    blockers = ledger_errors + policy_errors
    event_counts = Counter(row.get("event_type", "") for row in rows if row.get("event_type"))
    location_counts = Counter(row.get("location", "") for row in rows if row.get("location"))
    headings = [item["title"] for item in policy["headings"]]
    state = "REGENERATION_REQUIRED" if blockers else "REVIEW"
    ledger_hash = sha256_file(ledger_path)
    policy_hash = sha256_file(policy_path)

    citations: list[dict[str, Any]] = []
    if ledger["row_count"]:
        citations.append({
            "source": ledger_path.name,
            "sha256": ledger_hash,
            "locator": "CSV data rows 2..N",
            "claim": f"parsed {ledger['row_count']} records",
            "kind": "deterministic",
        })
    for heading in policy["headings"]:
        citations.append({
            "source": policy_path.name,
            "sha256": policy_hash,
            "locator": f"line {heading['line']}",
            "claim": f"Markdown heading: {heading['title']}",
            "kind": "policy",
        })

    if blockers:
        recommendations = [{
            "owner": "input-owner",
            "steps": ["修复输入文件中的阻塞项", "重新运行本脚本", "由制度或业务负责人复核输出"],
            "acceptance_criteria": ["阻塞项清零", "输入来源和版本可追溯", "复核人确认结果适用范围"],
        }]
        unresolved = [{"item": error, "reason": "输入准入失败"} for error in blockers]
    else:
        recommendations = [{
            "owner": "policy-owner",
            "steps": ["核对确定性统计与制度适用范围", "补充证据或处理冲突", "由授权人员决定是否采取后续动作"],
            "acceptance_criteria": ["每项结论有来源定位", "未决问题有责任人", "授权人员完成人工复核"],
        }]
        unresolved = [{
            "item": "人工复核与最终处置",
            "reason": "本地执行器不作授权、派单、关单、收费或其他外部写入",
        }]

    return {
        "schema": "evidence-governance/review-packet/v1",
        "task_profile": "joint_governance_analysis",
        "runner_version": RUNNER_VERSION,
        "terminal_state": state,
        "limitations": [
            "The runner does not interpret unknown columns or resolve policy-version conflicts.",
            "REVIEW is not approval or completion; human review remains required.",
        ],
        "input_snapshot": {
            "sources": [
                source_snapshot(ledger_path, "structured_records"),
                source_snapshot(policy_path, "policy_document"),
            ],
            "required_fields": list(REQUIRED_FIELDS),
            "recommended_fields": list(RECOMMENDED_FIELDS),
            "ledger": ledger,
            "policy": policy,
        },
        "deterministic_findings": {
            "event_type_counts": dict(sorted(event_counts.items())),
            "location_counts": dict(sorted(location_counts.items())),
            "policy_headings": headings,
            "blockers": blockers,
        },
        "recommendations": recommendations,
        "citations": citations,
        "unresolved_items": unresolved,
        "execution_boundary": "deterministic local review only; no model, network, database, or external write",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a deterministic evidence-governance review packet")
    parser.add_argument("--ledger", required=True, type=Path, help="CSV structured-record input")
    parser.add_argument("--policy", required=True, type=Path, help="Markdown policy input")
    parser.add_argument("--output", required=True, type=Path, help="JSON review-packet output")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_path = args.output.resolve()
    if output_path in {args.ledger.resolve(), args.policy.resolve()}:
        print(json.dumps({"status": "REGENERATION_REQUIRED", "error": "output must not overwrite an input file"}, ensure_ascii=False))
        return 2
    packet = build_packet(args.ledger, args.policy)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": packet["terminal_state"], "output": str(args.output)}, ensure_ascii=False))
    return 0 if packet["terminal_state"] == "REVIEW" else 2


if __name__ == "__main__":
    raise SystemExit(main())











