# VC Demo Script: VCW Workspace Sandbox

## One-Line Framing

VCW Workspace is an approval-gated agentic workflow framework for community operations. It reads messy operational signals from existing tools, proposes structured updates, and only writes after human approval and drift checks.

## Three-Minute Demo

1. Open the demo page:

   `sandbox/demo/vc-demo.html`

2. Start with the problem:

   "Community ops live across Gmail, Telegram, Google Sheets, CRM, Luma, and content automation. The pain is not one missing SaaS tool. The pain is that context is scattered and operators manually reconcile it."

3. Show the product flow:

   "The framework reads approved sources, extracts signal, proposes updates, waits for approval, drift-checks, then writes only approved changes."

4. Show the fake messages:

   "These are sandbox Gmail and Telegram examples. They are fake, but shaped like the real inputs: venue replies, team constraints, content status, and CRM context."

5. Show the approval queue:

   "The agent does not write directly. It produces proposal cards with target field, expected value, proposed value, confidence, and rationale."

6. Show fake-approved writes:

   "After simulated approval, six sheet updates apply. Three are skipped safely: Relay CRM is proposal-only in the sandbox, and drift detection prevents overwriting a field that changed earlier in the same run."

7. Show the fake Events Sheet after:

   "The sandbox sheet now has Warehouse West for AI Builders Salon and Culver Hub for HardTech Demo Night. No real Gmail, Telegram, Google Sheet, or CRM was touched."

## The Investor Point

This is not a chatbot. It is a workflow control layer:

- agents do reading, extraction, matching, and proposal drafting
- humans approve dangerous actions
- deterministic code handles writes
- drift checks prevent overwriting humans
- every action is auditable
- the same pattern can repeat across venue, speaker prep, sponsors, and outreach

## Live Commands

Run the full mixed demo:

```bash
python3 scripts/run_sandbox.py --scenario mixed-with-relay --approve-all
python3 scripts/build_sandbox_demo.py
```

Run Gmail-only:

```bash
python3 scripts/run_sandbox.py --scenario gmail-venue-replies --approve-all
python3 scripts/build_sandbox_demo.py
```

Run Telegram-only:

```bash
python3 scripts/run_sandbox.py --scenario telegram-ops-notes
```

## Safety Line

"The sandbox proves the architecture without credentials. Production adapters can be swapped in later, but the control model stays the same: propose first, approve explicitly, drift-check, then write."
