# VCW Workspace Sandbox

This sandbox mirrors the live `workspace-framework` workflow without touching Gmail, Telegram, Google Sheets, Relay CRM, Luma, or newsletter/social automation.

Use it to test the full community-ops framework with fake data:

- event-ops signal extraction
- venue workstream proposals
- Gmail reply tracking
- Relay CRM update planning
- content automation status visibility
- human approval queues
- drift checks
- audit logs

## Safety Contract

- No real API credentials.
- No live writes.
- No personal inbox data.
- No Telegram sends.
- No Google Sheet writes.
- No Relay CRM writes.
- No private keys, cookies, passwords, or tokens.

Everything runs from local JSON fixtures in this folder.

## Run

From the repo root:

```bash
python3 scripts/run_sandbox.py
```

This creates proposed updates only.

## Interactive Product Demo

Open this file in the browser:

`sandbox/demo/operator-console.html`

Use it as the live sandbox product demo:

1. Choose a scenario.
2. Click `Generate Proposals`.
3. Approve or reject individual proposals.
4. Watch the fake Events Master Sheet update.
5. Show the audit log and roadmap panel.

This is the easiest demo for investors because it behaves like an operator console rather than a terminal script.

To simulate approval and write to the sandbox sheet state:

```bash
python3 scripts/run_sandbox.py --approve-all
```

## Run Different Examples

List the available sandbox scenarios:

```bash
python3 scripts/run_sandbox.py --list-scenarios
```

Run Gmail as its own example:

```bash
python3 scripts/run_sandbox.py --scenario gmail-venue-replies
```

Run Telegram as its own example:

```bash
python3 scripts/run_sandbox.py --scenario telegram-ops-notes
```

Run content automation visibility as its own example:

```bash
python3 scripts/run_sandbox.py --scenario content-status
```

Run the full mixed example:

```bash
python3 scripts/run_sandbox.py --scenario mixed-with-relay
```

You can combine any scenario with `--approve-all` to simulate approval:

```bash
python3 scripts/run_sandbox.py --scenario gmail-venue-replies --approve-all
```

Outputs are written to:

- `sandbox/queue/approval_queue.json`
- `sandbox/queue/sandbox_sheet_after.json`
- `sandbox/audit/sandbox_audit_log.jsonl`

## Fixture Map

- `fixtures/gmail_messages.json`: fake Gmail event/venue replies.
- `fixtures/telegram_messages.json`: fake Telegram ops notes.
- `fixtures/events_sheet_snapshot.json`: fake Events Master Sheet state.
- `fixtures/relay_contacts.json`: fake Relay CRM contact records.
- `fixtures/luma_events.json`: fake Luma event history for venue memory.
- `fixtures/content_status.json`: fake newsletter/social automation visibility.
- `scenarios/*.json`: source toggles for Gmail-only, Telegram-only, content-only, and mixed examples.

## What This Proves

The sandbox proves the orchestration pattern before touching real systems:

1. Read approved sources.
2. Route signals to narrow skills.
3. Propose cell-level or record-level changes.
4. Require approval before writes.
5. Detect drift before applying a write.
6. Log every action.
