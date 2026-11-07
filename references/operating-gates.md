# Operating gates

These gates are the portable form of the source project's safety and runtime checks. A failed gate must be visible in the result.

## 1. Truth and evidence gate

Do not state a fact unless it is present in an admitted source or clearly marked as an inference. After new evidence, re-check the plan and affected conclusions.

## 2. Source and provenance gate

Every finding and policy match needs a source identifier and location. Preserve revision/date and source hash when available. Never resolve a conflict by silently choosing the first source.

## 3. Proposal/execution gate

An agent may propose an action and its acceptance criteria. It must not claim to have charged, dispatched, closed, merged, or otherwise executed a high-risk action.

## 4. Human review gate

Require human review for high-risk findings, unresolved conflicts, policy ambiguity, missing mandatory evidence, and final closure. A review decision must include reviewer identity/role, decision, reason, and time.

## 5. Degradation gate

If a model, provider, parser, or optional connector fails, preserve the deterministic baseline, record the failure class, and identify what remains unverified. Do not replace a failed result with invented content.

## 6. Snapshot binding gate

Bind analysis and review to the admitted input snapshot and policy revision. If the source set changes, create a new version rather than silently modifying a completed result.

## 7. Privacy and privilege gate

Do not disclose credentials, raw private files, unadmitted records, or provider connection details to a model or public artifact. Keep permissions limited to the requested read/analysis task.

## 8. Outcome gate

Only a verified outcome may be used for learning or performance claims. Do not automatically update policy, thresholds, or reputation from an unverified report.
