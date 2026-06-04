# State Schema

`state.json` is the local data contract for the dashboard. It is intentionally plain JSON so teams can inspect, copy, redact, and version the operating model without needing a backend.

The public repo includes a larger sanitized `state.json` plus a compact starter example at `examples/demo-state.json`.

## Design Principles

- Keep source data, proposed actions, and approved writes separate.
- Use stable IDs for records that appear across pages.
- Store demo fixtures and production credentials separately.
- Treat every external write as a proposal until a human approves it.
- Run `python3 scripts/privacy_audit.py` before publishing any changed state.

## Top-Level Shape

| Key | Type | Purpose |
|---|---|---|
| `generated_at` | string | Timestamp or label for the state snapshot. |
| `now` | object | Current operating focus, next action, and immediate risk. |
| `products` | array | Major operating lanes such as events, venues, sponsors, and content. |
| `work_status` | object | Cross-lane status counts and review metadata. |
| `sheet_sync` | object | Demo sheet-sync state, freshness, and proposed updates. |
| `newsletter_automation` | object | Content workflow status, links, feedback, and draft state. |
| `embeds` | array | Embedded sandbox/demo surfaces shown in the dashboard. |
| `events` | object | Event pipeline records and next actions. |
| `venues` | object | Venue memory, criteria, outreach, and decision state. |
| `sponsors` | object | Sponsor prospects, fit scoring, and follow-up state. |
| `pipeline` | object | Relationship, lead, or workstream pipeline summary. |
| `cost_scenarios` | object | AI/API cost planning assumptions and scenarios. |
| `learning` | array | Operator lessons, playbooks, or internal training notes. |
| `notes` | array | Short operational notes and review prompts. |
| `projects` | array | Project cards surfaced in the dashboard. |
| `tools` | array | Tool inventory, links, statuses, and use cases. |
| `premium_stack` | array | Paid or high-leverage tool stack notes. |
| `agents` | array | Agent definitions, constraints, and review needs. |
| `sources` | array | Source registry and trust level by system. |
| `memory` | array | Durable lessons and recap records. |
| `ideas` | array | Lightweight idea backlog. |
| `ideas_v2` | array | Structured idea backlog for newer views. |
| `automations` | array | Automation candidates and safety state. |
| `local_llm` | array | Local model or infrastructure notes. |
| `retros` | array | Retrospectives and workflow lessons. |
| `todos` | array | Action items surfaced to the operator. |
| `ops_entity` | object | Generic team or workspace metadata. |
| `team_pulse` | object | Team-level health, risks, and cadence notes. |

## Common Record Fields

Most arrays can use the same base pattern:

| Field | Purpose |
|---|---|
| `id` | Stable lowercase identifier. |
| `name` or `title` | Human-readable label. |
| `status` | Current state: `active`, `blocked`, `watch`, `done`, or a module-specific status. |
| `owner` | Generic role or team member responsible for review. |
| `priority` | Relative importance, usually `must`, `should`, or `watch`. |
| `next_action` | Concrete next move. |
| `source` | Source system or fixture that produced the signal. |
| `updated_at` | Snapshot date or review date. |
| `notes` | Short operator context. |

## Human Approval Fields

Use these fields when an agent proposes an external action:

| Field | Purpose |
|---|---|
| `proposal_id` | Stable ID for the proposed write. |
| `source_id` | Record or fixture that produced the proposal. |
| `action_type` | `draft`, `sheet_update`, `message`, `calendar_hold`, or similar. |
| `risk_level` | `low`, `medium`, or `high`. |
| `requires_approval` | Always `true` for external writes. |
| `approval_status` | `pending`, `approved`, `rejected`, or `needs_more_context`. |
| `rollback_note` | How to undo or ignore the action. |
| `audit_note` | What happened after review. |

## Source Registry

Sources should make trust and write boundaries explicit.

```json
{
  "id": "event-sheet-demo",
  "name": "Event Sheet Demo",
  "type": "spreadsheet_fixture",
  "trust_level": "demo",
  "read_policy": "allowed",
  "write_policy": "approval_required",
  "notes": "Synthetic fixture only."
}
```

## Cost Scenario Fields

Cost records should separate assumptions from observed billing.

| Field | Purpose |
|---|---|
| `scenario` | Demo, monthly cadence, or high-volume cadence. |
| `model` | Model or provider label. |
| `call_sites` | Workflow steps that create model/API calls. |
| `estimated_calls` | Planning volume. |
| `estimated_cost` | Planning estimate, not invoice truth. |
| `control` | How a team can reduce cost or cadence. |

## Starter State

Use `examples/demo-state.json` when you want a compact reference without the full public demo state.

Suggested path:

1. Copy `examples/demo-state.json` into a private working file.
2. Replace only generic demo labels first.
3. Add real records only in a private repo or local folder.
4. Keep credentials and live links outside JSON.
5. Run the privacy audit before any public export.

## Public Safety

Do not publish:

- API keys, OAuth tokens, webhooks, or bearer tokens
- private Google Sheet, document, CRM, event, or calendar URLs
- personal contact lists
- private local file paths
- live attendee, sponsor, founder, venue, or customer records
- screenshots or generated logs that contain private context
