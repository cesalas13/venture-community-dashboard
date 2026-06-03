# Privacy Model

Venture Community Ops is designed as a local-first public template. The public repo should show the workflow shape without exposing a real community's private operating data.

## Data Classes

| Class | Examples | Public repo rule |
|---|---|---|
| Demo data | fake events, fake venues, fake contacts, example queues | allowed |
| Sanitized structure | route names, schema shape, workflow categories | allowed |
| Private identifiers | sheet IDs, doc IDs, CRM IDs, local paths, repo URLs | not allowed |
| Private records | attendees, founders, sponsors, venues, emails, chats | not allowed |
| Credentials | API keys, OAuth tokens, webhooks, bearer tokens | not allowed |
| Generated logs | model prompts, raw outputs, browser screenshots | review before sharing |

## Local-First Assumption

The safest default is:

- static HTML app
- local `state.json`
- local sandbox fixtures
- no credentials in the repository
- no live writes from demo flows
- explicit approval before any external action

## Human Approval Boundary

Agents can help with:

- reading synthetic or approved local data
- summarizing workflow status
- drafting outreach
- proposing sheet or CRM changes
- estimating cost
- detecting drift

Agents should not automatically:

- send email
- message a team or external contact
- write to a production sheet
- update CRM records
- publish newsletter or social content
- create calendar events
- alter payment or ticketing systems

## Public Export Checklist

Before publishing a change:

```bash
python3 scripts/privacy_audit.py
git diff --check
git status --short
```

Review any touched files for:

- real names
- private event labels
- private venue names
- private emails or phone numbers
- private URLs
- private local paths
- generated logs
- screenshots
- hidden metadata

## Recommended Private Deployment Pattern

Keep a private working copy for real operations and export only sanitized demos into the public repo.

Suggested split:

- private repo or local folder: real state, credentials, live integration config
- public repo: app shell, docs, fake fixtures, sanitized schema examples
- generated public exports: run privacy audit before commit
