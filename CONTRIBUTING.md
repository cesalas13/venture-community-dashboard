# Contributing

Thanks for considering a contribution.

This project is early-stage, so the best contributions are practical and safety-oriented:

- clearer setup docs
- better sandbox fixtures
- privacy audit improvements
- reusable workflow templates
- UI fixes that keep the dashboard dense and operator-focused
- tests for route, state, and sandbox behavior

## Local Setup

```bash
git clone https://github.com/cesalas13/venture-community-dashboard.git
cd venture-community-dashboard
python3 -m http.server 8877 --bind 127.0.0.1
```

Open:

```text
http://127.0.0.1:8877/index.html#/home
```

## Before Opening A Pull Request

Run:

```bash
python3 scripts/privacy_audit.py
python3 scripts/eval_sandbox_dashboard.py
python3 -m json.tool state.json >/dev/null
python3 -m py_compile scripts/eval_sandbox_dashboard.py scripts/ops-server.py scripts/sync-event-master.py scripts/privacy_audit.py
git diff --check
```

If you change sandbox JavaScript:

```bash
find embeds/sandbox/demo -name '*.js' -type f -exec node --check {} \;
```

## Contribution Rules

- Keep examples synthetic or sanitized.
- Do not commit credentials, private links, private local paths, or live operational records.
- Prefer small, reviewable changes.
- Preserve the human-in-the-loop model.
- Add docs when adding a new workflow surface.
- Add or update checks when changing privacy-sensitive behavior.

## Good First Issues

- Add a more complete demo state import/export guide.
- Add additional fake-data sandbox scenarios.
- Add screenshot documentation with redacted demo data.
- Improve the privacy audit with more detector classes.
- Add a localStorage backup/restore example.
