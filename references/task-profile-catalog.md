# Task profile catalog

The source project defines five profiles. The domain nouns can be replaced while keeping the contract.

| Profile | Required role | Required fields | Main outputs | Review |
|---|---|---|---|---|
| `governance_event_summary` | governance ledger | `event_type` | total and grouped counts | citations, evidence, human review |
| `location_risk_assessment` | governance ledger | `event_type`, `location` | location counts and risk evidence | citations, linked recommendations, human review |
| `policy_clause_extraction` | policy document | none | clauses and scope gaps | paragraph citations and human review |
| `joint_governance_analysis` | ledger + policy document | ledger `event_type`, `location` | counts, clauses, evidence matches, gaps | linked recommendations and human review |
| `maintenance_summary` | maintenance log | `asset_id`, `operation`, `occurred_at` | operation totals and grouped counts | citations and human review |

Every profile must declare required roles, required/optional fields, allowed outputs, output types, citation requirements, evidence requirements, recommendation fields, and terminal states.

Do not choose a profile only from a keyword. Confirm the source roles and required fields first. If multiple profiles appear relevant, ask the user to choose or explain the combined contract explicitly.

## Source mapping

The originating project used `parking_conflict_risk` for the second row. This public contract renames it to `location_risk_assessment` so the workflow is not tied to parking or cycling. The required fields and review obligations are unchanged.

The other source profile IDs are preserved as public IDs because they are already domain-neutral: `governance_event_summary`, `policy_clause_extraction`, `joint_governance_analysis`, and `maintenance_summary`.

Unknown fields should be retained and reported as warnings. If multiple aliases could map to the same canonical field, stop for human confirmation instead of selecting by alias order.
