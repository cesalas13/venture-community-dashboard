# Operator Guide

This guide explains how to use the demo as an operator-facing control plane.

## Run Locally

```bash
python3 -m http.server 8877 --bind 127.0.0.1
```

Open:

```text
http://127.0.0.1:8877/index.html#/home
```

## Recommended Review Path

1. Start on Home to inspect current workflow status.
2. Open product and workstream pages to see each operations lane.
3. Review cost scenarios before increasing automation cadence.
4. Open sandbox demos before imagining live integrations.
5. Review approval queue examples before wiring writes.
6. Read `docs/privacy-model.md` before replacing demo data.

## What To Customize First

For a real team, customize in this order:

1. Product lanes: events, venues, speakers, sponsors, content, relationships.
2. Source registry: which tools are source of truth.
3. Approval policy: what agents may propose and what humans must approve.
4. Cost assumptions: model, cadence, call sites, and volume.
5. Demo fixtures: fake data that resembles your actual workflow shape.

## What To Avoid

- Do not paste secrets into `state.json`.
- Do not commit live contact lists.
- Do not connect a write path before adding approval and rollback.
- Do not publish screenshots without checking for private tabs or browser data.
- Do not treat model cost estimates as exact billing data.

## Public Demo Story

A useful demo narrative:

1. Show the dashboard overview.
2. Pick one workflow, such as venue scouting.
3. Show the source signal and proposed action.
4. Show the approval queue.
5. Show the sandbox result.
6. Explain the privacy boundary and human approval model.
