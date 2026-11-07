# Input and output contracts

## Input inventory

Before analysis, record:

```yaml
task_profile: stable identifier
sources:
  - id: stable source id
    role: governance_ledger | policy_document | maintenance_log
    revision: source revision or unknown
    hash: content hash or unknown
    locations: [sheet/row/column or paragraph/block references]
required_fields: []
mapping_decisions: []
limitations: []
```

Supported source types in the originating project include CSV, XLSX, JSON, DOCX, TXT, and Markdown. A consumer may support fewer formats, but it must state the limitation before analysis.

## Finding contract

Each finding should contain:

- `id`;
- `type` (`fact`, `risk`, `gap`, `conflict`, or `inference`);
- `statement`;
- `severity` or `priority` when applicable;
- `citations` with source and location;
- `uncertainty` or `limitations`;
- `review_state`.

## Recommendation contract

Each recommendation must include:

- the finding or evidence it addresses;
- `owner`;
- ordered `steps`;
- measurable `acceptance` criteria;
- dependencies or required approvals;
- citations and unresolved assumptions.

## State and terminal contract

Use these states:

- REVIEW — a deterministic packet was generated and is awaiting human review; it is not approval or completion;
- COMPLETED — reviewed, accepted, and supported by closure evidence;
- REJECTED — reviewed and rejected with reason;
- REGENERATION_REQUIRED — requires new analysis against a new or corrected snapshot.

Do not report an unreviewed REVIEW result as completed.
