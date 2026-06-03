# Venture Community Ops

Local-first operations dashboard for venture communities, accelerators, founder networks, and ecosystem teams.

This project turns the recurring work behind a venture community into a reusable control plane: events, venue scouting, speaker prep, sponsor tracking, newsletter status, relationship follow-up, approval queues, cost modeling, and agent-assisted workflow review.

It is built as a public-safe demo system. The included data is synthetic or sanitized, and the app is designed around human approval before any real-world write.

## Why This Exists

Community operations usually sprawl across spreadsheets, email, chat, event tools, CRM notes, docs, and ad hoc automations. That makes it hard to answer simple operator questions:

- Which events need attention?
- Which venue, speaker, sponsor, or newsletter workflows are blocked?
- What can an agent draft safely, and what still needs human approval?
- What would this workflow cost if it moved from demo mode to production cadence?
- Which systems are source of truth, and which are only previews?

Venture Community Ops packages those surfaces into one dashboard that a small team can inspect, customize, and extend.

## Who It Is For

- Venture community operators
- Accelerator and founder-program teams
- Ecosystem teams running recurring events
- Startup platform teams
- Developer-relations or founder-relations teams
- Builders studying practical human-in-the-loop AI operations

## What The Dashboard Covers

| Area | What it shows |
|---|---|
| Event ops | Event sheet status, pipeline notes, approvals, source health |
| Venue scouting | Venue memory, outreach drafts, reply tracking, decision criteria |
| Speaker prep | Bio gaps, panel questions, prep docs, briefing drafts |
| Sponsors | Prospecting, fit scoring, one-pagers, thank-you and renewal drafts |
| Newsletter/content | Issue status, link workflow, feedback loop, content automation status |
| Relationship follow-up | Stale contacts, warm-intro ideas, purpose-driven outreach |
| Approval queues | Proposed writes, drift checks, human review gates |
| Cost modeling | Scenario-level AI/API cost estimates across product lines |
| Sandbox demos | Fake Gmail, Telegram, Relay, Luma, and sheet fixtures for safe demos |

## Human-In-The-Loop Model

The core operating principle is simple:

> Agents may read, summarize, draft, score, and propose. Humans approve writes.

The demo includes approval queues, proposed updates, deterministic write scripts, cost assumptions, and sandbox fixtures so teams can test the operating model without touching live systems.

## Quickstart

Clone the repo:

```bash
git clone https://github.com/cesalas13/venture-community-dashboard.git
cd venture-community-dashboard
```

Open the static dashboard:

```bash
python3 -m http.server 8877 --bind 127.0.0.1
```

Then open:

```text
http://127.0.0.1:8877/index.html#/home
```

Stop the local server with `Ctrl+C`.

## Run The Checks

```bash
python3 scripts/privacy_audit.py
python3 scripts/eval_sandbox_dashboard.py
python3 -m json.tool state.json >/dev/null
python3 -m py_compile scripts/eval_sandbox_dashboard.py scripts/ops-server.py scripts/sync-event-master.py
```

Optional JavaScript syntax check:

```bash
find embeds/sandbox/demo -name '*.js' -type f -exec node --check {} \;
```

## Repository Layout

```text
.
├── index.html                     # static dashboard app
├── state.json                     # sanitized demo state
├── workspace-logo.svg             # generic workspace logo
├── embeds/sandbox/                # fake-data demo surfaces and fixtures
├── scripts/
│   ├── eval_sandbox_dashboard.py  # dashboard and sandbox evaluator
│   ├── privacy_audit.py           # public-safety scan
│   ├── ops-server.py              # optional local chat server scaffold
│   └── sync-event-master.py       # demo sheet snapshot sync helper
├── docs/
│   ├── case-study.md
│   ├── privacy-model.md
│   ├── workflows.md
│   └── operator-guide.md
├── examples/
│   └── event-ops-demo.md
└── ROADMAP.md
```

## Customizing It

Start with `state.json`. The dashboard reads structured records for products, projects, tools, cost scenarios, approval queues, workstreams, sources, and retros.

Safe customization path:

1. Copy `state.json` to a private working file.
2. Replace demo event, venue, sponsor, and newsletter records with your own local data.
3. Keep live credentials outside the repo.
4. Run `python3 scripts/privacy_audit.py` before committing.
5. Use sandbox fixtures before wiring any live integration.

## Security And Privacy

This repo is intentionally public-safe. It should not contain:

- API keys or OAuth tokens
- private Google Sheet URLs or document IDs
- private local paths
- personal contact lists
- private event labels
- live customer, founder, venue, sponsor, or attendee data
- generated logs with private prompts or model outputs

See [SECURITY.md](SECURITY.md) and [docs/privacy-model.md](docs/privacy-model.md).

## Open Source Status

This is an early-stage public template extracted from a richer private operations workflow. The goal is to make a useful, inspectable reference for local-first, agent-assisted operations systems.

Start with [docs/case-study.md](docs/case-study.md) for the public evaluation frame.

Near-term work is tracked in [ROADMAP.md](ROADMAP.md).

## Responsible Use

This project is an operations dashboard and workflow template. It is not a replacement for human judgment, legal review, security review, or operational accountability.

Use it to inspect workflows, demo approval loops, and prototype operations systems. Do not connect it to live systems until you have explicit approval gates, credential handling, audit logging, and rollback paths.

## License

MIT. See [LICENSE](LICENSE).
