# Runtime contract catalog

This catalog is a documentation-only translation of the nine source manifests. Tool names are descriptive references, not required integrations for this Skill. The neighboring run-spec files intentionally use a small set of public aggregate failure codes; those codes are a knowledge-layer normalization and must not be mistaken for additional source implementation error codes. Use this catalog for exact source-level fields and the run-specs for portable public behavior.

| ID | Inputs → outputs | Permission boundary | Budget/retry | Failure codes | Validators |
|---|---|---|---|---|---|
| `spreadsheet-quality-audit` | xlsx → quality report, field candidates, source ranges | document read | 1 call / 60s / retry 1 | unsupported format; invalid Office; formula cache missing; ambiguous fields | workbook openable; source ranges present; no formula-as-zero |
| `governance-record-analysis` | xlsx/csv/json → metrics, findings, citations | document read; analysis run | 3 calls / 120s / retry 1 | required field missing; ambiguous scope; no rows | metrics recomputable; citations valid |
| `governance-risk-assessment` | xlsx/docx/csv/json → risk findings, level, citations | document read; analysis run | 5 calls / 240s / retry 2 | insufficient evidence; conflicting sources; policy unknown | deterministic risk formula; visible conflict; citations valid |
| `policy-document-extract` | docx/txt/md → headings, paragraphs, tables, citations | document read; policy read | 2 calls / 120s / retry 1 | invalid Office; tracked revisions; empty document | document openable; logical locations present |
| `policy-evidence-match` | docx/xlsx/csv/json → evidence matches, citations, gaps | document read; policy read; analysis run | 3 calls / 180s / retry 1 | policy not found; evidence gap; invalid citation | every claim sourced; source revision matches |
| `recommendation-compose` | risk findings/citations → recommendations, limitations, citations | analysis read; proposal write | 2 calls / 120s / retry 0 | missing findings; proposal requires approval | no unreferenced claim; proposal is not execution |
| `artifact-consistency-verify` | docx/xlsx/report model → consistency report, export verification | artifact read | 0 calls / 60s / retry 0 | content mismatch; citation mismatch; file not openable | same input hash; same revision; same citations |
| `word-report-export` | report model/citations → docx/export verification | artifact write | 1 call / 120s / retry 1 | export failed; invalid citation; document not openable | document openable; content consistent; citations valid |
| `excel-action-register-export` | report model/recommendations/citations → xlsx/export verification | artifact write | 1 call / 120s / retry 1 | export failed; invalid citation; workbook not openable | workbook openable; content consistent; no formula injection; citations valid |

When this catalog is used without the original application, treat `calls`, `timeout`, and `retry` as risk-budget guidance rather than commands. A consumer must still preserve the permission boundary and failure behavior.
