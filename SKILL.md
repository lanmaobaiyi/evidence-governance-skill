---
name: evidence-governance
description: Apply an evidence-first governance workflow to structured records and policy documents. Use when an agent must classify inputs, check admission requirements, preserve citations, assess risks, compose accountable recommendations, or decide when human review is required. Do not use this skill to execute high-risk actions, operate a live service, or replace an authoritative policy owner.
---

# Evidence governance

Use this skill to turn governance records and policy documents into traceable analysis and review-ready recommendations. Keep the workflow deterministic by default and treat model reasoning as optional interpretation.

## Operating sequence

1. Identify the user goal, document roles, accepted formats, and requested task profile.
2. Check file integrity, parseability, source identity, date/revision, and required fields. Stop when a source cannot be located or safely interpreted.
3. Build an input inventory and immutable evidence snapshot. Record source identifiers, locations, and hashes when available.
4. Select one task profile from [references/task-profile-catalog.md](references/task-profile-catalog.md). Do not silently combine profiles.
5. Produce the deterministic baseline first: counts, mappings, extracted clauses, evidence matches, limitations, and citations.
6. If the user explicitly requests semantic enhancement, use only the admitted evidence snapshot. Never provide raw files, credentials, base URLs, or unadmitted material to a model.
7. Validate every finding and recommendation against [references/evidence-and-citations.md](references/evidence-and-citations.md) and [references/input-output-contracts.md](references/input-output-contracts.md).
8. Apply the gates in [references/operating-gates.md](references/operating-gates.md) and, for closure claims, [references/closure-evidence-checklist.md](references/closure-evidence-checklist.md). Stop, ask for evidence, degrade to the deterministic result, or require human review when a gate fails.
9. Return a review-ready result. Mark each item as evidence, inference, recommendation, limitation, or unresolved question. Do not claim that a proposed action was executed.

## Required output

Return:

- task profile and input snapshot summary;
- deterministic findings and their citations;
- risks, gaps, or conflicts with confidence/uncertainty stated plainly;
- recommendations with owner, steps, and acceptance criteria;
- model mode and fallback reason, if enhancement was attempted;
- human review decision and unresolved items;
- a clear state: REVIEW for an unapproved review packet, COMPLETED only after closure evidence and human authorization, or REJECTED/REGENERATION_REQUIRED when a gate fails.

Read only the references needed for the current task. Start with [the workflow](references/workflow.md) and [human review and fallback](references/human-review-and-fallback.md). For risk work, also read references/operating-gates.md, references/evidence-and-citations.md, and references/run-specs/analysis-risk.md. For policy work, read references/run-specs/evidence-policy.md. For exports, read references/run-specs/recommendation-export.md. Read references/run-specs/catalog.md when a concrete input/output, permission, retry, or failure contract is needed.

## Hard boundaries

- Never invent a citation, field, policy clause, execution result, or verified outcome.
- Never treat model output as a replacement for deterministic counts or source text.
- Never infer that a missing source means the policy permits an action.
- Never execute, authorize, close, dispatch, charge, or otherwise perform a high-risk action through this skill.
- Never learn from an unverified outcome or silently update a policy.

## Deterministic local runner

For a structured CSV ledger and a Markdown policy, run:

    python scripts/run_governance_case.py --ledger input.csv --policy policy.md --output review.json

The runner reads local files only, computes SHA-256 hashes, counts records by event and location, cites Markdown headings, and writes a JSON review packet. It does not use a model, network, database, or external write. Valid input produces REVIEW; admission failures produce REGENERATION_REQUIRED. Semantic interpretation, policy-version conflict resolution, and final authorization still require the workflow above and human review.

