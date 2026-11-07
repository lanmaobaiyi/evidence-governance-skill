# Run spec: recommendation and export

**Purpose:** turn reviewed findings into accountable follow-up and a portable report.

**Inputs:** reviewed findings, citations, limitations, and task profile.

**Outputs:** recommendations with `owner`, `steps`, and `acceptance`; review state; export-ready report.

**Failure codes:** `finding_not_evidenced`, `recommendation_incomplete`, `review_missing`, `artifact_inconsistent`.

**Validators:** recommendation links to a finding; required fields are present; report citations resolve; export cannot imply approval when review is incomplete.

**Review:** only `COMPLETED` results may be presented as approved outputs. Rejected or regenerated results remain traceable.
