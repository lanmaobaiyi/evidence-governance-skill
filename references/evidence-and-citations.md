# Evidence and citations

## Citation rules

1. Cite the smallest useful source location: worksheet/cell, CSV row, JSON path, document paragraph, or Markdown heading.
2. Keep the source revision/hash with the citation when available.
3. Every claim in a finding, risk, policy match, or recommendation must point to one or more citations.
4. If a claim is derived from multiple records, state the aggregation rule and the contributing source set.
5. If a source cannot be located, downgrade the claim to an unresolved question or remove it.

## Conflicts

Make conflicting values visible. State which source is newer or authoritative only when a documented rule supports that choice. Otherwise stop for human resolution.

## Model boundary

Models may summarize, classify, or relate information inside the admitted evidence package. They may not alter source counts, create citations, infer missing permissions, or receive raw credentials and unadmitted files.

## Evidence quality labels

- `direct`: the source explicitly states the fact;
- `calculated`: a deterministic calculation over cited records;
- `matched`: a claim matched to a cited policy clause;
- `inferred`: an interpretation that needs review;
- `missing`: required evidence was not supplied.

## Optional output guardrails

For model-enhanced review packets, adopters may cap the response at three findings and three recommendations, with at most two evidence references per item. If an item has no valid citation, return an empty result for that item and mark the evidence as insufficient. These limits are safety defaults from the source project, not a replacement for the adopting organization's policy.
