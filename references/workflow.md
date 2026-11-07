# Evidence-first workflow

## Purpose

Use a repeatable sequence that keeps facts, interpretations, recommendations, and decisions separate.

## Sequence

1. **Intake** — state the goal, expected output, source roles, time range, and decision owner.
2. **Admission** — verify format, parseability, source identity, revision/date, required fields, and ambiguous mappings.
3. **Snapshot** — record the admitted source set, field mapping, source locations, limitations, and a digest/hash when available.
4. **Baseline** — calculate deterministic counts, distributions, clause extraction, evidence links, and missing data.
5. **Optional enhancement** — use a model only for interpretation over the snapshot; preserve the baseline unchanged.
6. **Validation** — check output types, source references, conflict visibility, recommendation closure, and policy revision match.
7. **Review** — send unresolved or high-impact items to a human reviewer; record the decision and reason.
8. **Close** — export only a review-approved result and preserve the snapshot and citations.

## Stop conditions

Stop and ask for clarification when a required role or field is missing, two sources conflict without a resolution rule, a citation cannot be located, or the requested action exceeds the evidence. Return a degraded deterministic result when optional model enhancement fails.

## State labels

- `CREATED`: a result exists but is not reviewed;
- `REVIEW`: a human decision is required;
- `COMPLETED`: a reviewer approved the result;
- `REJECTED`: the result was rejected with a reason;
- `REGENERATION_REQUIRED`: the input snapshot or analysis must be revised without overwriting the prior result.
