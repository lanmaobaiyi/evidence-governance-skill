# Run spec: policy and evidence

**Purpose:** extract policy clauses and match admitted records or findings to them.

**Inputs:** policy document plus optional admitted ledger/maintenance records.

**Outputs:** clauses, applicability/scope, evidence matches, gaps, and citations.

**Failure codes:** `policy_not_found`, `policy_unknown`, `evidence_gap`, `citation_invalid`, `revision_mismatch`.

**Validators:** every claim has a source; every match records the source revision and location; conflicts remain visible.

**Review:** human review is required when applicability, exceptions, or source authority is ambiguous.
