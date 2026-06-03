# Event Ops Demo

This example shows how a venture community event workflow can move through the dashboard without using live systems.

## Scenario

A founder event needs venue confirmation, speaker prep, sponsor follow-up, and newsletter visibility.

## Inputs

- Fake event sheet row
- Fake Gmail venue reply
- Fake team chat note
- Fake event-platform history
- Fake newsletter status record

## Agent-Proposed Outputs

- Update event status from `venue scouting` to `venue hold needs approval`.
- Add venue capacity and pricing note.
- Draft venue confirmation reply.
- Flag speaker prep gaps.
- Add newsletter status note.

## Human Approval

The operator reviews:

- whether the venue reply matches the right event
- whether the proposed status update is accurate
- whether the outreach draft is appropriate
- whether any cost or contract detail needs manual confirmation

Only after approval should a production system be updated.

## Demo Files

Relevant sandbox files:

- `embeds/sandbox/fixtures/events_sheet_snapshot.json`
- `embeds/sandbox/fixtures/gmail_messages.json`
- `embeds/sandbox/fixtures/telegram_messages.json`
- `embeds/sandbox/queue/approval_queue.json`
- `embeds/sandbox/queue/sandbox_sheet_after.json`

## Lessons

- Keep source data and proposed writes separate.
- Make every proposed write reviewable.
- Preserve drift checks.
- Keep demo fixtures fake.
- Treat external messages as drafts until a human approves them.
