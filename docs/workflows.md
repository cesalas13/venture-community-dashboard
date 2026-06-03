# Workflow Model

Venture Community Ops groups community operations into repeatable workflow lanes.

## Core Pattern

Each lane follows the same human-in-the-loop path:

```text
source signal -> agent read/summarize -> draft/proposal -> human review -> approved write -> audit note
```

## Event Ops

Purpose: keep the event pipeline visible and reduce manual sheet maintenance.

Example signals:

- event sheet rows
- inbox replies
- team chat notes
- event platform status
- content workflow status

Safe agent outputs:

- event status summary
- proposed sheet update
- drift warning
- approval digest

Human approval required for:

- sheet writes
- external messages
- calendar changes
- event page edits

## Venue Scouting

Purpose: rank venue options and track outreach.

Safe agent outputs:

- venue comparison
- outreach draft
- reply summary
- decision criteria checklist

Human approval required for:

- sending outreach
- confirming holds
- signing agreements
- updating production venue records

## Speaker Prep

Purpose: prepare speaker context and reduce prep-call overhead.

Safe agent outputs:

- bio gap list
- panel question draft
- prep doc outline
- briefing email draft

Human approval required for:

- emailing speakers
- publishing bios
- changing agenda or speaker commitments

## Sponsor Ops

Purpose: manage sponsor research, fit, follow-up, and renewal.

Safe agent outputs:

- prospect list
- fit score rationale
- one-pager outline
- thank-you draft
- renewal prompt

Human approval required for:

- sponsor outreach
- pricing or package commitments
- CRM writes
- public sponsor mentions

## Newsletter And Content

Purpose: keep content production visible without rebuilding every automation.

Safe agent outputs:

- issue status
- missing links
- feedback summary
- recap draft

Human approval required for:

- publishing newsletter content
- sending campaigns
- updating source-of-truth docs

## Relationship Follow-Up

Purpose: identify stale relationships and draft useful re-engagement.

Safe agent outputs:

- stale-contact report
- warm-intro ideas
- purpose-driven draft

Human approval required for:

- sending messages
- changing CRM stages
- assigning owners

## Cost Tracking

Purpose: make AI and API usage visible before automations scale.

The included cost scenarios model:

- demo usage
- active monthly cadence
- higher-volume operating cadence
- cost control options

Use these as planning estimates, not invoices.
