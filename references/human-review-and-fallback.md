# Human review and fallback

## Review packet

Give the reviewer the input snapshot, deterministic baseline, citations, model execution status, unresolved conflicts, recommendations, and explicit decisions requested. Do not ask a reviewer to infer missing evidence from a polished summary.

## Required review points

- ambiguous field or role mappings;
- insufficient or conflicting evidence;
- high-risk classification;
- recommendations that affect rights, access, safety, money, or service closure;
- final approval for export or closure.

For closure claims, apply [the closure evidence checklist](closure-evidence-checklist.md). A polished report is not a substitute for `CHECKIN`, `FUNCTIONAL_TEST`, `OBSERVATION`, and `HUMAN_REVIEW` evidence.

## Fallback behavior

When optional enhancement fails:

1. keep the deterministic baseline;
2. record `requested_mode` and `effective_mode`;
3. record provider/model status only at the level needed for diagnosis;
4. state what semantic interpretation is missing;
5. preserve the human review path.

When deterministic analysis cannot complete, return a structured failure with the missing input, failure code, and recovery request. Never fabricate a partial success.

## Learning boundary

Only verified outcomes may become examples or evaluation evidence. Policy updates remain manual; a report may recommend a change but cannot apply it.
