# Security Policy

## Supported Scope

This project is a public-safe demo and template for local-first operations workflows. Security review focuses on:

- secret exposure
- accidental private data in demo state
- unsafe examples that imply live writes without approval
- local path or repository leakage
- public docs that encourage insecure credential handling

## Reporting Issues

Open a GitHub issue for non-sensitive bugs.

For sensitive findings, do not paste secrets or private records into a public issue. Instead, describe the class of issue and the affected file path without exposing the data itself.

## Public Data Rules

Public commits should not include:

- API keys, OAuth tokens, webhook URLs, or bearer tokens
- private Google Sheet, Drive, Calendar, Gmail, Telegram, CRM, or event-system identifiers
- private local or home-directory paths
- private contact lists, venue contacts, sponsor contacts, attendee data, or founder records
- production approval queues or generated agent logs
- screenshots containing private browser tabs, emails, calendars, chats, or dashboards

## Required Checks Before Release

Run:

```bash
python3 scripts/privacy_audit.py
python3 scripts/eval_sandbox_dashboard.py
git diff --check
git status --short
```

For code changes, also run:

```bash
python3 -m py_compile scripts/eval_sandbox_dashboard.py scripts/ops-server.py scripts/sync-event-master.py scripts/privacy_audit.py
find embeds/sandbox/demo -name '*.js' -type f -exec node --check {} \;
```

## Live Integrations

This repo should treat every live integration as opt-in. Agents may draft or propose, but any live write to email, sheets, CRM, chat, calendar, docs, payments, or event systems should require a human approval gate and an audit trail.
