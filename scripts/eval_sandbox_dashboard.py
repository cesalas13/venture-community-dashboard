#!/usr/bin/env python3
"""Local evals for the workspace dashboard sandbox surface."""

from __future__ import annotations

import re
import os
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


DASH_DIR = Path(__file__).resolve().parents[1]
INDEX = DASH_DIR / "index.html"
DEMO_DIR = DASH_DIR / "embeds" / "sandbox" / "demo"
BASE_URL = "http://127.0.0.1:8766"

PRODUCTS = {
    "Event Ops": "./embeds/sandbox/demo/operator-console.html?scenario=telegram-ops-notes&simple=1&assetV=20260519-clickable",
    "Venue": "./embeds/sandbox/demo/operator-console.html?scenario=gmail-venue-replies&simple=1&assetV=20260519-clickable",
    "Newsletter": "./embeds/sandbox/demo/newsletter-console.html?simple=1&assetV=20260519-clickable",
    "Speaker Prep": "./embeds/sandbox/demo/workstream-products.html?product=speaker&simple=1&assetV=20260519-clickable",
    "Sponsors": "./embeds/sandbox/demo/workstream-products.html?product=sponsors&simple=1&assetV=20260519-clickable",
    "Outreach": "./embeds/sandbox/demo/workstream-products.html?product=outreach&simple=1&assetV=20260519-clickable",
}

EMBEDS = {
    "/index.html": "Dashboard Manual",
    "/embeds/sandbox/demo/operator-console.html": "Run the VCW workflow without touching real systems.",
    "/embeds/sandbox/demo/newsletter-console.html": "newsletter workflow",
    "/embeds/sandbox/demo/workstream-products.html": "Workstream Products",
    "/embeds/sandbox/demo/run-surfaces.html": "Run Surfaces",
    "/embeds/sandbox/demo/vc-demo.html": "VCW Workspace Sandbox",
}


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def ok(message: str) -> None:
    print(f"ok: {message}")


def read(path: Path) -> str:
    if not path.exists():
        fail(f"missing file: {path}")
    return path.read_text(encoding="utf-8")


def assert_local_embed_assets() -> None:
    for html_path in sorted(DEMO_DIR.glob("*.html")):
        html = read(html_path)
        for attr in re.findall(r"""(?:href|src)=["']([^"']+\.(?:css|js)(?:\?[^"']*)?)["']""", html):
            asset_name = attr.split("?", 1)[0]
            asset = html_path.parent / asset_name
            if not asset.exists():
                fail(f"{html_path.name} references missing asset {attr}")
    ok("all sandbox HTML CSS/JS references exist")


def assert_dashboard_wiring() -> None:
    index = read(INDEX)
    for name, url in PRODUCTS.items():
        if url not in index:
            fail(f"{name} sandbox URL not found in index.html")
        if "assetV=20260519-clickable" not in url:
            fail(f"{name} sandbox URL is not cache-busted")
    for fragment in ("#speaker", "#sponsors", "#outreach"):
        if fragment in index:
            fail(f"product sandbox URL still contains scrolling fragment {fragment}")
    for required in (
        "setSandboxFrameSrc",
        "restoreDashboardScroll",
        "e.preventDefault();",
        "frame.replaceWith(replacement)",
    ):
        if required not in index:
            fail(f"dashboard missing sandbox wiring guard: {required}")
    ok("dashboard sandbox wiring prevents default jumps and replaces stale iframes")


def assert_dashboard_links() -> None:
    index = read(INDEX)
    pages = set(re.findall(r'<section[^>]+class=["\'][^"\']*\bpage\b[^"\']*["\'][^>]+data-page=["\']([^"\']+)["\']', index))
    if not pages:
        fail("no dashboard pages found")

    routes: set[str] = set()
    relative_links: set[str] = set()
    external_links = 0
    native_links = 0

    for href in re.findall(r'href=["\']([^"\']+)["\']', index):
        href = href.strip()
        if not href or href.startswith(("javascript:", "mailto:", "tel:")):
            continue
        if href.startswith("#/"):
            route = href[2:].split("?", 1)[0].split("#", 1)[0]
            routes.add(route)
            if route not in pages:
                fail(f"internal route {href} has no matching section[data-page]")
        elif href.startswith("./"):
            relative_links.add(href)
            clean = href.split("?", 1)[0].split("#", 1)[0]
            if not (DASH_DIR / clean[2:]).exists():
                fail(f"relative hyperlink target is missing: {href}")
        elif href.startswith(("http://", "https://")):
            external_links += 1
            if not urllib.parse.urlparse(href).netloc:
                fail(f"malformed external hyperlink: {href}")
        elif href.startswith("workspace://"):
            native_links += 1
            host = urllib.parse.urlparse(href).hostname or ""
            if host not in {"claude", "open-url"}:
                fail(f"unknown workspacedash native link host: {href}")
        elif href.startswith("file://"):
            path = urllib.parse.unquote(urllib.parse.urlparse(href).path)
            if path and not Path(path).exists():
                fail(f"file hyperlink target is missing: {href}")

    for page in ("home", "overview", "future-plans", "sandbox", "workflow", "projects", "pipeline", "automations"):
        if page not in pages:
            fail(f"required page missing: {page}")

    ok(f"dashboard hyperlinks: {len(routes)} internal routes, {len(relative_links)} local files, {external_links} external URLs, {native_links} native links")


def assert_search_in_upper_nav() -> None:
    index = read(INDEX)
    sidebar = re.search(r"<aside class=\"sidebar\">(.*?)</aside>", index, re.S)
    if not sidebar:
        fail("dashboard is missing the upper sidebar/header nav")
    if 'id="search-input"' not in sidebar.group(1):
        fail("search input is not in the upper tab/header row")
    topbar = re.search(r"<div class=\"topbar\">(.*?)</div>\s*\n\n  <!--", index, re.S)
    if topbar and 'id="search-input"' in topbar.group(1):
        fail("search input is still inside the lower topbar")
    if ".sidebar > .search" not in index:
        fail("search input is missing upper-nav sizing CSS")
    for required in (
        'id="search-panel"',
        'aria-controls="search-panel"',
        "function buildSearchIndex()",
        "function renderSearchPanel()",
        "data-search-result",
        "refreshSearchFilteredViews();",
    ):
        if required not in index:
            fail(f"search input is missing live results wiring: {required!r}")
    ok("search input sits in the upper tab/header row and has live results")


def assert_inline_javascript_syntax() -> None:
    index = read(INDEX)
    scripts: list[str] = []
    for match in re.finditer(r"<script(?P<attrs>[^>]*)>(?P<body>.*?)</script>", index, re.I | re.S):
        attrs = match.group("attrs") or ""
        if "src=" in attrs.lower() or "application/json" in attrs.lower():
            continue
        body = match.group("body").strip()
        if body:
            scripts.append(body)
    node = subprocess.run(["/usr/bin/env", "node", "--version"], text=True, capture_output=True)
    if node.returncode != 0:
        fail("node is not available for inline JavaScript syntax checks")
    with tempfile.TemporaryDirectory(prefix="workspace-dashboard-js-") as tmp:
        tmp_path = Path(tmp)
        for index_num, script in enumerate(scripts):
            script_path = tmp_path / f"inline-{index_num}.js"
            script_path.write_text(script, encoding="utf-8")
            result = subprocess.run(["node", "--check", str(script_path)], text=True, capture_output=True)
            if result.returncode != 0:
                fail(f"inline JavaScript {index_num} failed syntax check: {(result.stderr or result.stdout).strip()}")
    ok(f"inline JavaScript syntax checks passed for {len(scripts)} script blocks")


def assert_workstream_embed_behavior() -> None:
    js = read(DEMO_DIR / "workstream-products.js")
    if "scrollIntoView" in js:
        fail("workstream product embed still calls scrollIntoView")
    for required in (
        "history.scrollRestoration = \"manual\"",
        "window.scrollTo({ top: 0",
        "requestedProduct",
    ):
        if required not in js:
            fail(f"workstream embed missing stable-scroll behavior: {required}")
    ok("workstream product embed does not auto-scroll to product sections")


def assert_demo_clickability() -> None:
    for html_path in sorted(DEMO_DIR.glob("*.html")):
        html = read(html_path)
        for tag in re.findall(r"<(?:button|select|a)\b[^>]*>", html, re.I):
            if re.search(r"\bdisabled\b", tag, re.I):
                fail(f"{html_path.name} has disabled clickable control: {tag}")
        for href in re.findall(r"<a\b[^>]*href=['\"]([^'\"]+)['\"]", html, re.I):
            if not href or href == "#":
                fail(f"{html_path.name} has inert anchor href: {href!r}")
        for src in re.findall(r"<script\b[^>]*src=['\"]([^'\"]+\.js(?:\?[^'\"]*)?)['\"]", html, re.I):
            if "?v=" not in src:
                fail(f"{html_path.name} script is not cache-busted: {src}")

    for js_path in sorted(DEMO_DIR.glob("*.js")):
        js = read(js_path)
        if re.search(r"\.disabled\s*=\s*true", js):
            fail(f"{js_path.name} disables a clickable control at runtime")
        if re.search(r"setAttribute\(\s*['\"]disabled['\"]", js):
            fail(f"{js_path.name} sets a clickable control disabled at runtime")

    operator_js = read(DEMO_DIR / "operator-console.js")
    for required in (
        'byId("scenarioSelect").addEventListener("change"',
        "state.scenarioKey = event.target.value",
        "renderAll();",
    ):
        if required not in operator_js:
            fail(f"operator console scenario box missing working change handler: {required}")
    ok("sandbox demo controls are not disabled or inert")


def assert_project_completion_sort() -> None:
    index = read(INDEX)
    for required in (
        "sorted by completion",
        "const progressA = projectProgress(a).pct;",
        "const progressB = projectProgress(b).pct;",
        "return progressB - progressA;",
    ):
        if required not in index:
            fail(f"project supporting records are not sorted by completion: missing {required!r}")
    ok("project supporting records sort by highest completion first")


def assert_cost_scenarios_state() -> None:
    import json

    state_path = DASH_DIR / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    cs = state.get("cost_scenarios")
    if not cs:
        fail("state.cost_scenarios is missing")
    for key in ("pricing", "scenarios", "totals", "products", "caveats", "methodology", "what_this_changes", "update_triggers"):
        if key not in cs:
            fail(f"state.cost_scenarios missing key: {key}")
    if len(cs["products"]) != 6:
        fail(f"expected 6 products in cost_scenarios, got {len(cs['products'])}")
    names = [p["name"] for p in cs["products"]]
    for name in ("Event Ops", "Venue", "Newsletter", "Speaker Prep", "Sponsors", "Outreach"):
        if name not in names:
            fail(f"cost_scenarios missing product: {name}")
    for p in cs["products"]:
        for k in ("name", "status", "cadence", "call_sites", "monthly", "cost_shape", "risk_vectors", "scenario_d_levers"):
            if k not in p:
                fail(f"product {p.get('name')} missing key: {k}")
        for scenario in ("A", "B", "C", "D"):
            if scenario not in p["monthly"]:
                fail(f"product {p['name']} missing monthly scenario {scenario}")
    for scenario in ("A", "B", "C", "D"):
        if scenario not in cs["totals"]:
            fail(f"cost_scenarios.totals missing scenario {scenario}")
    expected_totals = {"A": 3.24, "B": 17.45, "C": 52.40, "D": 5.75}
    for scenario, expected in expected_totals.items():
        actual = float(cs["totals"][scenario])
        if round(actual, 2) != expected:
            fail(f"cost_scenarios.totals.{scenario} expected {expected:.2f}, got {actual:.2f}")
    ok("state.cost_scenarios shape valid (6 products, all scenarios, all call_sites)")


def assert_home_future_plan_sections() -> None:
    index = read(INDEX)
    def page_html(page: str) -> str:
        match = re.search(
            rf'<section class="page" data-page="{re.escape(page)}">(.*?)(?=\n  <!-- ───────────|\n  <section class="page"|</main>)',
            index,
            re.S,
        )
        if not match:
            fail(f"missing page section for {page}")
        return match.group(1)

    home = page_html("home")
    overview = page_html("overview")
    future = page_html("future-plans")
    products = page_html("projects")
    workflow = page_html("workflow")

    for required in (
        'href="#/home"',
        'href="#/future-plans"',
        ">Manual</a>",
        "Quick options",
        "Where to go",
        "Operating context",
    ):
        if required not in index:
            fail(f"dashboard is missing home/future navigation or home content: {required!r}")
    for required in (
        "Venture Community Automated Operations",
        "Quick options",
        "Where to go",
        "This is where you open the Telegram approval gate and review drafted changes before anything moves forward.",
        "Operating context",
        "Todos",
        'id="todos-list"',
        'id="todo-new-task"',
        'id="todo-toggle"',
        'id="todo-summary"',
        'id="todo-body"',
        "Inputs, notes, learnings, and ideas",
    ):
        if required not in home:
            fail(f"home page missing requested content: {required!r}")
    if not (home.index("Operating context") < home.index("Todos") < home.index("Start here") < home.index("Quick options") < home.index("Where to go")):
        fail("home page order is wrong: Operating context must lead into Todos, Start here, Quick options, and Where to go")
    for required in (
        "Dashboard Manual",
        "How to use the workspace dashboard.",
        "Only the newsletter automation is treated as live, and it is still WIP.",
        "Home",
        "Products",
        "Human in the loop",
        "Future Plans",
        "Sandbox",
        "Where the old overview cards moved.",
    ):
        if required not in overview:
            fail(f"manual page missing beginner content: {required!r}")
    for required in (
        "Possible mediums + future notes",
        'data-future-tab="action-plan"',
        'data-future-panel="action-plan"',
        "Sandbox proves the flow; live products still need SOP context.",
        "Granola",
        "Telegram",
        "Gmail",
        "Prompt assembly avoids new API spend.",
        "Roadmap questions",
        "Use simulations to decide what is worth building next.",
        "Simulate scenarios using cheap models, premium models, local LLMs, prompt assembly, and hybrid routing",
        "Practical source and automation tool list used by modern teams.",
        "Notion, Airtable, Coda, Google Sheets",
        "n8n, Zapier, Make, Relay.app, Workato",
        "only matter if a partner requires integration",
        "$40/month",
        'aria-label="Future plan notes editor"',
        'id="future-note-form"',
        'data-future-note-dropdown',
        'id="future-note-product-trigger"',
        'data-future-note-menu',
        'id="future-note-body"',
        'id="future-note-list"',
        "SAVE NOTE",
        'data-future-tab="costs"',
        'data-future-panel="costs"',
        "Automation cost procedure map",
        "Pipeline Cost Snapshot",
        "Measured spend from the live pipeline.",
        "Scenario A $3.24/mo",
        'id="pipeline-vs-scenario"',
        "Six-product cost scenarios",
        'class="cost-scenarios"',
        'id="cost-scenario-cards"',
        'id="cost-matrix"',
        'id="cost-product-panels"',
        'id="cost-method"',
        'id="cost-pricing-table"',
        'id="cost-changes"',
        'id="cost-caveats"',
        'id="cost-update-triggers"',
        "Per-product scenario matrix",
        "Methodology",
        "What this changes for the rest of the cost plan",
        "Update triggers",
        "source: ../workspace-framework/docs/cost-optimization-plan/07-six-product-cost-scenarios.md",
        "The old overview pipeline card is a future planning and cost-control surface",
        "n8n, inputs, and approved output paths",
        "#/automations",
        "Requires access to the n8n account",
        "Terminal handoff",
    ):
        if required not in future:
            fail(f"future plans page missing requested section: {required!r}")
    for required in (
        "Products",
        "Event sheet, agenda, day-of run",
        "Generate, hyperlinks, schedule",
        "Each card is a business workflow with its own live surface and safe demo.",
        "Shared human in the loop",
        "Human in the loop · all products",
        "Needs Decision",
        "Scout, outreach, reply tracking",
        "Progress and supporting records",
        'id="products-grid"',
    ):
        if required not in products:
            fail(f"products page missing product-owned surface/status content: {required!r}")
    for required in (
        'id="venue-scouting-builder"',
        'id="venue-scout-location"',
        'id="venue-scout-generate"',
        'id="venue-scouting-matrix"',
        'id="venue-call-list"',
        "COPY MATRIX",
        "Venue scouting automation",
    ):
        if required not in index:
            fail(f"dashboard missing venue product-detail builder content: {required!r}")
    if "How work moves" not in workflow:
        fail("Route Work page is missing the How work moves flow")
    for moved in (
        "How work moves",
        "Possible mediums + future notes",
        "Automation cost procedure map",
        "n8n, inputs, and approved output paths",
        "Operating context",
        "Quick options",
        "Live work surfaces",
        "Workstream detail",
        "Pipeline Cost Snapshot",
        "Event Ops · Event Master Sheet",
        "Newsletter · Newsletter Automation",
        'id="product-overview-grid"',
        'id="mini-donut"',
        'id="mini-types"',
        'id="mini-stack"',
        "Six-product cost scenarios",
        "Per-product scenario matrix",
    ):
        if moved in overview:
            fail(f"overview still contains moved home/future/route content: {moved!r}")
    for forbidden in (
        "live Gmail, Sheets, or CRM",
        "No live Sheet, Gmail, or CRM",
        "Live write: update Sheets, CRM",
    ):
        if forbidden in index:
            fail(f"dashboard still implies CRM/Sheets/Gmail are live write surfaces: {forbidden!r}")
    for removed in (
        'id="kpi-active"',
        'id="kpi-paused"',
        "TIME LEFT</span>",
    ):
        if removed in index:
            fail(f"overview still contains duplicate calendar KPI card: {removed!r}")
    ok("home/future pages split overview content and keep duplicate event/time KPI cards removed")


def assert_operator_review() -> None:
    index = read(INDEX)
    state = read(DASH_DIR / "state.json")
    evaluator_doc = DASH_DIR / "docs" / "Operator-vc-owner-evaluator.md"
    if not evaluator_doc.exists():
        fail("missing Operator evaluator documentation")
    for required in (
        "Operator VC Check",
        "Operator-vc-owner-evaluator",
        "operator-review",
    ):
        if required not in state or required not in index:
            fail(f"Operator evaluator agent is not present in state and embedded dashboard: {required!r}")
    for required in (
        "Where Does This Go?",
        "Open newsletter sheet",
        "Progress and supporting records",
        "STALE BLOCKS",
        "AI helper",
        "Operator check",
        "Use Operator to find what would confuse a nontechnical operator",
        "agent-checklist",
        "Human in the loop",
        "Items waiting on you",
        "AI drafts wait for Telegram approval.",
        "it is not the live write button",
        "approval gate sends a numbered Telegram digest",
        "telegram-gate-tile",
        "Open VCW Ops Agent",
        "https://example.invalid/ops-agent",
        "Approval happens in your VCW Ops Telegram agent.",
        "approve 1 3",
        "reject default",
        "Reply approve all or approve numbers",
        "Rejects by default after timeout",
        "Inputs",
        "rule-based helper",
        "advanced AI helper",
        "review handoff records",
    ):
        if required not in index:
            fail(f"dashboard is missing nontechnical operator wording: {required!r}")
    try:
        render_agents = index[index.index("function renderAgents()"):index.index("function renderSources()")]
    except ValueError:
        fail("could not find renderAgents block for nontechnical wording checks")
    for forbidden in (
        "Open newsletter automation",
        "community newsletter Worfklow",
        "Workflow Router",
        "DRIFT BLOCKS",
        "haiku + sonnet",
        "AI drafts wait here. You approve, reject, or skip.",
        "hit approve, reject, or skip",
        "Approve, reject, or skip drafted changes",
        '<canvas id="agents-bar"></canvas>',
        "Start with Operator",
        "Operator Evaluator",
        "Review the dashboard like a busy venture capital firm owner",
    ):
        if forbidden in index or forbidden in state:
            fail(f"dashboard still exposes confusing operator wording: {forbidden!r}")
    for forbidden in (
        "id: ${a.name",
        "${a.kind",
        "${a.category === 'operator-review'",
    ):
        if forbidden in render_agents:
            fail(f"agents page still renders internal agent labels: {forbidden!r}")
    ok("Operator evaluator agent and nontechnical operator language are present")


def fetch(path: str) -> str:
    try:
        with urllib.request.urlopen(f"{BASE_URL}{path}", timeout=3) as response:
            if response.status != 200:
                fail(f"{path} returned HTTP {response.status}")
            return response.read().decode("utf-8", errors="replace")
    except urllib.error.URLError as exc:
        fail(f"could not fetch {path}: {exc}")


def assert_served_embeds() -> None:
    for path, marker in EMBEDS.items():
        body = fetch(path)
        if marker not in body:
            fail(f"{path} missing expected marker {marker!r}")
    ok("dashboard server returns every sandbox embed with expected content")


def assert_served_dashboard_markers() -> None:
    body = fetch("/index.html")
    for marker in (
        "Home",
        "Future Plans",
        "Only the newsletter automation is treated as live",
        "Sandbox Mode",
        "sandbox-product-link",
        "sorted by completion",
        "Operator VC Check",
        "Where Does This Go?",
        "Open newsletter sheet",
        "Venue scouting automation",
        "Los Angeles recreates the flagship dinner workbook shape",
        "Photo-sourced Git install queue",
        "photo-git-install-grid",
        "OrgLoop",
        "GitHub MCP Server",
        "GitHub Agentic Workflows",
        "OpenAI Agents SDK",
        "LangGraph",
        "Trigger.dev",
        "browser-use",
        "Automation cost procedure map",
        "#/automations",
        "assetV=20260519-clickable",
        "setSandboxFrameSrc",
        "restoreDashboardScroll",
        "history.scrollRestoration = 'manual'",
        "resetDashboardScroll",
        "forceDashboardScrollTop",
    ):
        if marker not in body:
            fail(f"served dashboard missing expected marker {marker!r}")
    ok("served dashboard contains live/sandbox markers and scroll guards")


def main() -> int:
    assert_local_embed_assets()
    assert_dashboard_links()
    assert_search_in_upper_nav()
    assert_inline_javascript_syntax()
    assert_dashboard_wiring()
    assert_workstream_embed_behavior()
    assert_demo_clickability()
    assert_project_completion_sort()
    assert_cost_scenarios_state()
    assert_home_future_plan_sections()
    assert_operator_review()
    if os.environ.get("WORKSPACE_DASHBOARD_EVAL_SERVED") == "1":
        assert_served_embeds()
        assert_served_dashboard_markers()
    else:
        ok("served checks skipped; set WORKSPACE_DASHBOARD_EVAL_SERVED=1 when serving this duplicate on BASE_URL")
    print("PASS: sandbox dashboard evals completed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
