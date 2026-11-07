# Expected review report (synthetic)

## Input snapshot

- Ledger: `synthetic-ledger.csv`, three records, source hash recorded by the consumer.
- Policy: `synthetic-policy.md`, sections `Scope`, `Response`, and `Review`.
- Profile: `joint_governance_analysis`.

## Deterministic findings

- `North Gate` has three recorded events in two rows: two `parking_conflict` units and one `blocked_access` unit. Cite the corresponding CSV rows.
- The policy requires an accessibility check and reviewer confirmation before closure. Cite the `Response` and `Review` sections.

## Recommendation

- **Owner:** duty reviewer
- **Steps:** verify the affected route, record the observation, and confirm the corrective step.
- **Acceptance:** the reviewer can locate the cited records, confirms the route is usable, and records the review decision.

## Review state

`REVIEW`: the synthetic records do not prove that the route was inspected or restored. Do not mark the case `COMPLETED`.
