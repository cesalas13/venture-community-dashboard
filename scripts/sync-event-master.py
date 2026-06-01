#!/usr/bin/env python3
"""Sync the VCW dashboard front-page date from the Events Master snapshot.

Run after:
  python3 ../workspace-framework/scripts/pull_snapshot.py

The script reads the local live-sheet snapshot and promotes the next dated
event into state.json so scripts/build.sh can embed it into index.html.
"""

import json
from collections import Counter
from datetime import date, datetime, timezone
from pathlib import Path

DASHBOARD = Path(__file__).resolve().parents[1]
STATE_PATH = DASHBOARD / "state.json"
SNAPSHOT_PATH = DASHBOARD / "embeds/sandbox/fixtures/events_sheet_snapshot.json"
EVENT_MASTER_URL = "#/sources"
NEWSLETTER_SHEET_URL = "#/sources"


def parse_sheet_date(value):
    if not value:
        return None
    text = str(value).strip()
    for fmt in ("%m/%d/%y", "%m/%d/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    return None


def iso_date(value):
    parsed = parse_sheet_date(value)
    return parsed.isoformat() if parsed else None


def next_event(events, today):
    candidates = []
    for event in events:
        event_date = parse_sheet_date(event.get("Date"))
        if event_date and event_date >= today:
            candidates.append((event_date, event))
    if candidates:
        return sorted(candidates, key=lambda item: item[0])[0]
    dated = [(parse_sheet_date(event.get("Date")), event) for event in events if parse_sheet_date(event.get("Date"))]
    return sorted(dated, key=lambda item: item[0])[-1] if dated else (None, {})


def main():
    state = json.loads(STATE_PATH.read_text())
    snapshot = json.loads(SNAPSHOT_PATH.read_text())
    events = snapshot.get("events", [])
    chosen_date, event = next_event(events, date.today())

    newsletter_counts = Counter((e.get("Newsletter Status") or "blank").strip() for e in events)
    event_name = event.get("Event") or "—"
    event_date = chosen_date.isoformat() if chosen_date else None
    sheet_row = event.get("_sheet_row")
    newsletter_status = (event.get("Newsletter Status") or "unscheduled").strip()

    state.setdefault("now", {})
    state["now"]["next_event"] = f"{event_name} · {event_date}" if event_date else event_name
    state["now"]["last_touched"] = "event master sync"

    state["sheet_sync"] = {
        "source_name": "Events Master Sheet",
        "source_url": EVENT_MASTER_URL,
        "sheet_id": "demo-event-tracker-id",
        "tab": "Calendar",
        "header_row": 7,
        "date_label": "EVENT DATE",
        "dashboard_date": event_date,
        "event_name": event_name,
        "event_status": event.get("Status") or "—",
        "newsletter_status": newsletter_status,
        "sheet_row": sheet_row,
        "row_count": snapshot.get("row_count", len(events)),
        "last_synced_at": snapshot.get("snapshot_at"),
        "status": "snapshot ready",
        "sync_command": "python3 ../workspace-framework/scripts/pull_snapshot.py && python3 scripts/sync-event-master.py",
        "next_step": "Refresh the Events Master snapshot, then run the dashboard sync script to promote the next dated event into the main page.",
    }

    state["newsletter_automation"] = {
        "name": "newsletter-v11",
        "status": "paused",
        "sheet_title": "community newsletter Worfklow (Automated)",
        "sheet_url": NEWSLETTER_SHEET_URL,
        "active_tab": "Generate",
        "active_gid": 1621685316,
        "current_issue": event_name,
        "event_date": event_date,
        "newsletter_status": newsletter_status,
        "featured_event_source": f"Events Master Sheet row {sheet_row}" if sheet_row else "Events Master Sheet",
        "scheduled_events": newsletter_counts.get("Scheduled", 0),
        "featured_events": newsletter_counts.get("Featured", 0),
        "skipped_events": newsletter_counts.get("Skipped", 0),
        "workflow": [
            {
                "label": "Generate",
                "detail": "Generate newsletter draft from the Generate tab plus Event Master featured event context.",
            },
            {
                "label": "Links",
                "detail": "Populate Hyperlinks tab, then apply approved URLs into the draft Doc.",
            },
            {
                "label": "Feedback",
                "detail": "Process Feedback tab into Elements voice rules before the next issue.",
            },
        ],
        "next_step": "Use the linked Generate tab as the first integrated automation example: unpause cadence, generate the synced issue, then run links and feedback.",
    }
    state["generated_at"] = datetime.now(timezone.utc).isoformat()
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n")
    print(f"Synced {event_name} ({event_date}) from row {sheet_row} into {STATE_PATH}")


if __name__ == "__main__":
    main()
