# Roadmap

Venture Community Ops is an early-stage public template. The roadmap focuses on making it more reusable for real teams while preserving privacy and human approval.

## Phase 1: Public Template Hardening

- Keep README, SECURITY, CONTRIBUTING, and workflow docs current.
- Maintain `scripts/privacy_audit.py` as a release gate.
- Maintain issue templates for bugs, feature requests, and privacy reports.
- Add screenshot docs using only sanitized demo data.
- Keep the MIT license file present and linked from the README.

## Phase 2: Reusable Operations Modules

- Event ops module: event status, owner, next action, approval history.
- Venue module: venue memory, scouting criteria, outreach drafts, reply status.
- Speaker module: bio gaps, panel questions, prep docs, briefing drafts.
- Sponsor module: prospects, fit scores, one-pagers, renewal prompts.
- Content module: newsletter status, links, feedback, recap workflow.
- Relationship module: stale contacts, warm intros, follow-up drafts.

## Phase 3: Local-First Data Model

- Document the `state.json` schema.
- Add `examples/demo-state.json` as a smaller starter state.
- Add import/export helpers for private local state.
- Add a redaction helper for public demo exports.

## Phase 4: Agent Workflow Safety

- Add explicit agent workflow cards for read, draft, propose, approve, write.
- Add approval queue examples for each module.
- Add rollback notes for every demo write path.
- Add audit-log examples that avoid private prompt leakage.

## Phase 5: Maintainer Automation

- Expand CI checks for privacy, syntax, JSON shape, and route integrity.
- Add a release checklist.
- Add scripted issue/PR triage helpers.
- Add documentation checks for stale links and missing examples.

## Long-Term Direction

The goal is a lightweight open-source operations control plane for venture communities and accelerator-style teams. It should remain easy to run locally, easy to inspect, safe to customize, and clear about which actions require human approval.
