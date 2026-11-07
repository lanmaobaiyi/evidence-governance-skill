# Run spec: analysis and risk

**Purpose:** produce deterministic summaries and risk findings from admitted records.

**Inputs:** admitted ledger or maintenance log, optional policy context, declared task profile.

**Outputs:** totals, distributions, risk findings, severity/priority, limitations, and citations.

**Failure codes:** `insufficient_evidence`, `conflicting_sources`, `policy_unknown`, `unsupported_profile`.

**Validators:** deterministic calculations are reproducible; risk formula/threshold is visible; no finding lacks a citation; uncertainty is explicit.

**Review:** any high-risk result, unresolved conflict, or recommendation affecting rights, safety, access, money, or closure requires human review.
