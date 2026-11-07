# Closure evidence checklist

Use this checklist for any result that claims a case, recommendation, or review cycle is complete. It is a portable abstraction of the source project's close protocol; it does not authorize a real-world action.

The evidence sequence is:

1. `CHECKIN` — the responsible operator or system reports the current state and scope;
2. `FUNCTIONAL_TEST` — the required function or control is checked against an observable criterion;
3. `OBSERVATION` — the result is observed for the required interval or sample set, with timestamps and source identity;
4. `HUMAN_REVIEW` — an authorized reviewer records `APPROVE_CLOSE`, `REJECT`, or `REGENERATION_REQUIRED` with identity, reason, and time.

Bind the checklist to the policy revision, decision snapshot, recovery evidence root, and input digest. A changed source or policy creates a new version; it must not silently rewrite an earlier result.

If any step or binding is missing, the terminal state cannot be `COMPLETED`. Return the missing evidence and use `REVIEW`, `REJECTED`, or `REGENERATION_REQUIRED` as appropriate. These are public abstraction labels; an implementation must map them to its own decision enum (the source project uses variants including `APPROVE`, `REJECT`, `REGENERATE`, and `APPROVE_CLOSE`).

The originating project also uses signed telemetry and numeric observation thresholds. Those are domain-specific implementation details and should be supplied by the adopting organization as an explicit policy appendix, never inferred by this Skill.
