# Case Study: Venture Community Operating System

This case study explains what the dashboard is meant to prove and how to evaluate it as a public-safe portfolio project.

## Problem

Venture community teams usually run high-context operations across scattered tools:

- event sheets
- venue notes
- sponsor tracking
- speaker prep docs
- newsletter status
- relationship follow-up
- chat threads
- approval decisions

The hard part is not building another dashboard. The hard part is preserving context, approval boundaries, and operating cadence when a small team has too many surfaces to watch.

## Product Thesis

The dashboard acts as a local-first control plane for venture community operations.

It should help an operator answer five questions quickly:

1. What needs attention right now?
2. Which source produced the signal?
3. What can an agent safely draft or propose?
4. What requires human approval before any write happens?
5. What evidence remains after the decision?

## Workflow Pattern

Every module follows the same operating loop:

```text
source signal -> structured summary -> proposed action -> human approval -> controlled write -> audit note
```

That loop is intentionally conservative. It lets the system demonstrate useful automation without pretending that agents should send messages, update production sheets, or alter records without review.

## Demo Scenario

A founder event is moving from planning to execution.

The dashboard surfaces:

- event status and owner
- venue scouting status
- speaker prep gaps
- sponsor follow-up tasks
- newsletter readiness
- approval queue items
- estimated automation cost

The operator reviews the proposed changes, approves only the correct ones, and leaves an audit note. The public repo uses synthetic records so this can be inspected without exposing a real event.

## Why Local-First Matters

The public template keeps the default workflow simple:

- static app shell
- local `state.json`
- sandbox fixtures
- no credentials
- no live writes
- explicit privacy audit before commit

That makes the project easy to run, easy to review, and safe to customize before a team connects live systems.

## Evaluation Checklist

Use this checklist when reviewing the project.

| Question | What good looks like |
|---|---|
| Does the app show real operator work? | Events, venues, speakers, sponsors, content, relationships, approvals, and cost are visible. |
| Is the agent boundary clear? | Agents read, summarize, draft, score, and propose. Humans approve writes. |
| Is demo data safe? | Data is synthetic or sanitized, with no credentials, private URLs, or live contacts. |
| Can a team customize it? | `state.json`, docs, sandbox fixtures, and workflows describe where to start. |
| Is there a release gate? | `scripts/privacy_audit.py` and local checks are documented. |

## What This Demonstrates

- Product judgment around high-context operations.
- Practical human-in-the-loop agent design.
- Public-safe extraction from a richer private workflow.
- Local-first architecture for sensitive operating data.
- Clear separation between demo fixtures and production systems.

## Next Strongest Improvements

1. Add a smaller starter `examples/demo-state.json`.
2. Document the public `state.json` schema.
3. Add screenshot docs using sanitized demo records only.
4. Add module-specific approval queue examples.
5. Add release checklist automation for privacy, JSON shape, and route integrity.
