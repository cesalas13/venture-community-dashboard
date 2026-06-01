const lanes = [
  {
    name: "Sandbox",
    status: "fake data",
    description: "Product demo lane. Fixtures in, local JSON out.",
    has: ["Gmail/Telegram/Luma/Relay/content fixtures", "approval queue simulation", "operator console"],
    doesNot: ["read live inboxes", "send Telegram", "write Sheets"],
  },
  {
    name: "Trial Run",
    status: "local model",
    description: "LM Studio and local Llama tests that exercise prompts without live sources.",
    has: ["tracked harnesses", "ignored receipts", ".env.local provider config"],
    doesNot: ["commit secrets", "touch live adapters", "pollute product queue"],
  },
  {
    name: "Real Product",
    status: "live",
    description: "Actual event ops and workstream runners with live adapters and approval gates.",
    has: ["Gmail reader", "Telegram reader", "event classifier", "approval gate", "sheet writer"],
    doesNot: ["skip human approval by default", "hide drift", "publish content automatically"],
  },
];

const products = [
  {
    name: "Event Ops",
    function: "Sync event signal from Gmail and Telegram into approved Sheet proposals.",
    sandbox: "operator-console.html?scenario=mixed-with-relay",
    trial: "trial-product-runs/runs/local_classifier_trial.py",
    real: "scripts/run_pipeline.py",
  },
  {
    name: "Venue Replies",
    function: "Turn inbound venue availability, holds, quotes, and constraints into approval-gated event updates.",
    sandbox: "operator-console.html?scenario=gmail-venue-replies",
    trial: "scripts/run_sandbox.py --scenario gmail-venue-replies",
    real: "scripts/process_venue_gmail_replies.py",
  },
  {
    name: "Venue Scouting",
    function: "Rank venue options against event needs before outreach or sponsor-ready recommendations.",
    sandbox: "skills/venue/fixtures/event-needs-venue.json",
    trial: "scripts/run_venue.py",
    real: "scripts/run_venue.py with approved data sources",
  },
  {
    name: "Newsletter / Content",
    function: "Mirror the existing Apps Script workflow: Generate, Elements, Feedback, Hyperlinks, Log, and readiness checks.",
    sandbox: "newsletter-console.html",
    trial: "docs/proposals/newsletter-automation-adapter.md",
    real: "read-only adapter planned",
  },
  {
    name: "Speaker Prep",
    function: "Create briefing docs, missing-info checks, and panel questions.",
    sandbox: "scripts/run_workstream_products.py --sandbox-copy",
    trial: "skills/speaker-prep/fixtures/speaker-prep-input.json",
    real: "draft-only product workstream",
  },
  {
    name: "Sponsors",
    function: "Draft sponsor follow-ups, one-pager inputs, and sponsor prospecting shortlists.",
    sandbox: "scripts/run_workstream_products.py --sandbox-copy",
    trial: "skills/sponsors/fixtures/*.json",
    real: "draft-only product workstream",
  },
  {
    name: "Outreach",
    function: "Find stale relationships and draft purpose-driven outreach.",
    sandbox: "scripts/run_workstream_products.py --sandbox-copy",
    trial: "skills/outreach/fixtures/*.json",
    real: "draft-only product workstream",
  },
];

const commands = [
  {
    lane: "Sandbox",
    command: "cd ./workspace-framework\n/opt/homebrew/bin/python3.12 scripts/run_sandbox.py --scenario mixed-with-relay --approve-all",
    note: "Safest product demo. No live systems.",
  },
  {
    lane: "Trial Run",
    command: "cd ./workspace-framework\n/opt/homebrew/bin/python3.12 trial-product-runs/runs/local_classifier_trial.py",
    note: "Calls local LM Studio through .env.local and writes an ignored JSON receipt.",
  },
  {
    lane: "Workstream Demo",
    command: "cd ./workspace-framework\n/opt/homebrew/bin/python3.12 scripts/run_workstream_products.py --sandbox-copy",
    note: "Builds speaker, sponsor, and outreach demo artifacts.",
  },
  {
    lane: "Real Product",
    command: "cd ./workspace-framework\n/opt/homebrew/bin/python3.12 scripts/run_pipeline.py",
    note: "Live adapters. Only run when ready for Gmail, Telegram, approval, and Sheet flow.",
  },
];

function renderLanes() {
  document.getElementById("laneGrid").innerHTML = lanes.map((lane) => `
    <article class="card">
      <header>
        <h3>${lane.name}</h3>
        <span class="status ${lane.name === "Real Product" ? "live" : lane.name === "Trial Run" ? "trial" : ""}">${lane.status}</span>
      </header>
      <p>${lane.description}</p>
      <strong>Has</strong>
      <ul>${lane.has.map((item) => `<li>${item}</li>`).join("")}</ul>
      <strong>Doesn't</strong>
      <ul>${lane.doesNot.map((item) => `<li>${item}</li>`).join("")}</ul>
    </article>
  `).join("");
}

function renderProducts() {
  document.getElementById("productGrid").innerHTML = products.map((product) => `
    <article class="card">
      <header>
        <h3>${product.name}</h3>
        <span class="status">mapped</span>
      </header>
      <p>${product.function}</p>
      <ul>
        <li><strong>Sandbox:</strong> ${product.sandbox.includes(".html") ? `<a href="${product.sandbox}"><code>${product.sandbox}</code></a>` : `<code>${product.sandbox}</code>`}</li>
        <li><strong>Trial:</strong> <code>${product.trial}</code></li>
        <li><strong>Real:</strong> <code>${product.real}</code></li>
      </ul>
    </article>
  `).join("");
}

function renderCommands() {
  document.getElementById("commandStack").innerHTML = commands.map((item) => `
    <article class="command">
      <div>
        <h3>${item.lane}</h3>
        <p>${item.note}</p>
      </div>
      <pre>${item.command}</pre>
    </article>
  `).join("");
}

renderLanes();
renderProducts();
renderCommands();
