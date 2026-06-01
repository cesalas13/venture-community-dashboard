const baseSheet = [
  {
    row_id: "evt_001",
    event_name: "AI Builders Salon",
    date: "2026-06-12",
    status: "venue scouting",
    venue: "",
    notes: "Needs projector, quiet room, sponsor-friendly layout.",
  },
  {
    row_id: "evt_002",
    event_name: "Climate Founders Dinner",
    date: "2026-06-26",
    status: "speaker prep",
    venue: "Existing Partner Loft",
    notes: "Dinner format. Confirm dietary constraints.",
  },
  {
    row_id: "evt_003",
    event_name: "HardTech Demo Night",
    date: "2026-07-10",
    status: "sponsor outreach",
    venue: "",
    notes: "Needs loading access and room for demo tables.",
  },
];

const scenarios = {
  "gmail-venue-replies": {
    label: "Venue Replies: Gmail holds + quotes",
    product: "Venue Replies",
    sources: ["gmail", "luma"],
    messages: [
      {
        id: "gm_001",
        source: "gmail",
        title: "Re: AI Builders Salon venue hold",
        body: "Warehouse West can hold June 12. Capacity 110 seated, projector included, venue fee $1800, Arts District. Need confirmation by Friday.",
      },
      {
        id: "gm_002",
        source: "gmail",
        title: "HardTech Demo Night",
        body: "Culver Hub can host July 10. Capacity 160, loading dock available, demo tables included. Quote is $2500 plus security.",
      },
    ],
    proposals: [
      {
        id: "prop_001",
        source: "gm_001",
        skill: "venue",
        target_id: "evt_001",
        field: "venue",
        expected: "",
        proposed: "Warehouse West",
        confidence: 0.91,
        rationale: "Matches date, capacity, Arts District preference, projector need, and prior Luma venue memory.",
      },
      {
        id: "prop_002",
        source: "gm_001",
        skill: "venue",
        target_id: "evt_001",
        field: "status",
        expected: "venue scouting",
        proposed: "venue hold needs approval",
        confidence: 0.86,
        rationale: "Venue offered a temporary hold and requires confirmation by Friday.",
      },
      {
        id: "prop_003",
        source: "gm_002",
        skill: "venue",
        target_id: "evt_003",
        field: "venue",
        expected: "",
        proposed: "Culver Hub",
        confidence: 0.89,
        rationale: "Matches July 10, Culver City preference, 160 capacity, loading dock, and demo tables.",
      },
      {
        id: "prop_004",
        source: "gm_002",
        skill: "venue",
        target_id: "evt_003",
        field: "notes",
        expected: "Needs loading access and room for demo tables.",
        proposed: "Needs loading access and room for demo tables. Culver Hub quote: $2500 plus security.",
        confidence: 0.84,
        rationale: "Adds quote and operational constraints from the venue reply.",
      },
    ],
  },
  "telegram-ops-notes": {
    label: "Telegram: team ops notes",
    product: "Event Ops",
    sources: ["telegram"],
    messages: [
      {
        id: "tg_001",
        source: "telegram",
        title: "Operator in vcw-ops",
        body: "For AI Builders Salon, prioritize Arts District venues under $2k if they have projector and sponsor-friendly layout.",
      },
      {
        id: "tg_002",
        source: "telegram",
        title: "Workspace Admin in vcw-ops",
        body: "HardTech needs loading access and enough room for demo tables. Culver City preferred.",
      },
    ],
    proposals: [
      {
        id: "prop_005",
        source: "tg_001",
        skill: "venue",
        target_id: "evt_001",
        field: "notes",
        expected: "Needs projector, quiet room, sponsor-friendly layout.",
        proposed: "Needs projector, quiet room, sponsor-friendly layout. Operator preference: Arts District under $2k.",
        confidence: 0.79,
        rationale: "Team-chat note adds decision criteria from Operator.",
      },
      {
        id: "prop_007",
        source: "tg_002",
        skill: "venue",
        target_id: "evt_003",
        field: "notes",
        expected: "Needs loading access and room for demo tables.",
        proposed: "Needs loading access, room for demo tables, and Culver City preference from Telegram ops.",
        confidence: 0.76,
        rationale: "Team-chat note adds requirements before venue outreach is finalized.",
      },
    ],
  },
  "mixed-with-relay": {
    label: "Mixed: Gmail + Telegram + Relay + content",
    product: "Event Ops Control Plane",
    sources: ["gmail", "telegram", "relay", "luma", "content"],
    messages: [],
    proposals: [],
  },
};

scenarios["mixed-with-relay"].messages = [
  ...scenarios["gmail-venue-replies"].messages,
  ...scenarios["telegram-ops-notes"].messages,
  {
    id: "rel_002",
    source: "relay",
    title: "Relay CRM contact: Culver Hub",
    body: "Relationship stage is new, but active venue reply and prior Luma event history suggest a warm-stage update should be proposed only.",
  },
  {
    id: "cnt_001",
    source: "content",
    title: "Newsletter status",
    body: "AI Builders Salon recap draft is queued in existing content automation. Framework should show visibility, not rebuild the content tool.",
  },
];

scenarios["mixed-with-relay"].proposals = [
  ...scenarios["gmail-venue-replies"].proposals,
  ...scenarios["telegram-ops-notes"].proposals,
  {
    id: "prop_006",
    source: "rel_002",
    skill: "relay-crm-update-planner",
    target_id: "rel_002",
    target_type: "relay_contact",
    field: "relationship_stage",
    expected: "new",
    proposed: "warm",
    confidence: 0.72,
    rationale: "CRM update is proposed but not applied inside this sandbox.",
    dangerous: true,
  },
  {
    id: "prop_008",
    source: "cnt_001",
    skill: "content-status-router",
    target_id: "evt_001",
    field: "notes",
    expected: "Needs projector, quiet room, sponsor-friendly layout.",
    proposed: "Needs projector, quiet room, sponsor-friendly layout. Content status: newsletter is draft queued.",
    confidence: 0.62,
    rationale: "Content automation is routed around; only visibility is proposed.",
  },
];

const state = {
  scenarioKey: new URLSearchParams(window.location.search).get("scenario") || "mixed-with-relay",
  sheet: structuredClone(baseSheet),
  proposals: [],
  audit: [],
};

function byId(id) {
  return document.getElementById(id);
}

function showToast(message) {
  const toast = byId("toast");
  toast.textContent = message;
  toast.classList.add("visible");
  window.setTimeout(() => toast.classList.remove("visible"), 1600);
}

function addAudit(action, detail) {
  state.audit.unshift({
    time: new Date().toLocaleTimeString(),
    action,
    detail,
  });
  renderAudit();
}

function renderScenarios() {
  byId("scenarioSelect").innerHTML = Object.entries(scenarios)
    .map(([key, scenario]) => `<option value="${key}">${scenario.product ? `${scenario.product} - ` : ""}${scenario.label}</option>`)
    .join("");
  byId("scenarioSelect").value = state.scenarioKey;
}

function renderMetrics() {
  const approved = state.proposals.filter((proposal) => proposal.status === "approved").length;
  const rejected = state.proposals.filter((proposal) => proposal.status === "rejected").length;
  const applied = state.proposals.filter((proposal) => proposal.applied).length;
  const skipped = state.proposals.filter((proposal) => proposal.skipped).length;
  byId("metrics").innerHTML = [
    ["Product", scenarios[state.scenarioKey].product || "Sandbox"],
    ["Scenario", scenarios[state.scenarioKey].label],
    ["Proposals", state.proposals.length],
    ["Approved", approved],
    ["Applied / Skipped", `${applied} / ${skipped}`],
    ["Rejected", rejected],
    ["Live writes", "0"],
  ]
    .map(([label, value]) => `<article class="metric"><span>${label}</span><strong>${value}</strong></article>`)
    .join("");
}

function renderMessages() {
  byId("messageGrid").innerHTML = scenarios[state.scenarioKey].messages
    .map((message) => `
      <article class="message-card">
        <span class="tag">${message.source}</span>
        <h3>${message.title}</h3>
        <p>${message.body}</p>
      </article>
    `)
    .join("");
}

function renderProposals() {
  const html = state.proposals.length
    ? state.proposals
        .map((proposal) => {
          const status = proposal.status || "waiting";
          const statusClass = proposal.dangerous ? "danger" : status === "approved" ? "good" : status === "rejected" ? "danger" : "warn";
          return `
            <article class="proposal-card">
              <div class="proposal-top">
                <span class="tag ${statusClass}">${status}</span>
                <span class="pill">${proposal.confidence}</span>
              </div>
              <h3>${proposal.skill} · ${proposal.field}</h3>
              <p><strong>Target:</strong> ${proposal.target_id}</p>
              <p><strong>Expected:</strong> ${proposal.expected || "blank"}</p>
              <p><strong>Proposed:</strong> ${proposal.proposed}</p>
              <p>${proposal.rationale}</p>
              <div class="proposal-actions">
                <button type="button" data-approve="${proposal.id}">Approve</button>
                <button type="button" class="ghost" data-reject="${proposal.id}">Reject</button>
              </div>
            </article>
          `;
        })
        .join("")
    : `<article class="proposal-card"><h3>No proposals yet</h3><p>Choose a scenario and click Generate Proposals.</p></article>`;

  byId("proposalGrid").innerHTML = html;
  document.querySelectorAll("[data-approve]").forEach((button) => {
    button.addEventListener("click", () => approveProposal(button.dataset.approve));
  });
  document.querySelectorAll("[data-reject]").forEach((button) => {
    button.addEventListener("click", () => rejectProposal(button.dataset.reject));
  });
}

function renderSheet() {
  byId("sheetBody").innerHTML = state.sheet
    .map((row) => `
      <tr>
        <td>${row.event_name}</td>
        <td>${row.date}</td>
        <td>${row.status}</td>
        <td>${row.venue || "<em>blank</em>"}</td>
        <td>${row.notes}</td>
      </tr>
    `)
    .join("");
}

function renderAudit() {
  byId("auditLog").innerHTML = state.audit.length
    ? state.audit
        .map((item) => `<article class="audit-item"><span>${item.time} · ${item.action}</span><p>${item.detail}</p></article>`)
        .join("")
    : `<article class="audit-item"><span>waiting</span><p>No sandbox actions yet.</p></article>`;
}

function renderAll() {
  renderMetrics();
  renderMessages();
  renderProposals();
  renderSheet();
  renderAudit();
}

function generateProposals() {
  state.sheet = structuredClone(baseSheet);
  state.proposals = scenarios[state.scenarioKey].proposals.map((proposal) => ({ ...proposal, status: "waiting", applied: false, skipped: false }));
  state.audit = [];
  addAudit("generated", `${state.proposals.length} proposals from ${scenarios[state.scenarioKey].label}.`);
  showToast("Proposals generated");
  renderAll();
}

function approveProposal(id) {
  const proposal = state.proposals.find((item) => item.id === id);
  if (!proposal || proposal.status === "approved") return;
  proposal.status = "approved";

  if (proposal.target_type === "relay_contact") {
    proposal.skipped = true;
    addAudit("skipped", `${proposal.id} was approved but not applied because CRM writes are disabled in sandbox.`);
    showToast("Approved but skipped safely");
    renderAll();
    return;
  }

  const row = state.sheet.find((item) => item.row_id === proposal.target_id);
  if (!row) {
    proposal.skipped = true;
    addAudit("skipped", `${proposal.id} target row was not found.`);
    renderAll();
    return;
  }

  if (row[proposal.field] !== proposal.expected) {
    proposal.skipped = true;
    addAudit("drift", `${proposal.id} skipped: expected "${proposal.expected || "blank"}" but found "${row[proposal.field] || "blank"}".`);
    showToast("Drift detected");
    renderAll();
    return;
  }

  row[proposal.field] = proposal.proposed;
  proposal.applied = true;
  addAudit("applied", `${proposal.id}: ${proposal.target_id}.${proposal.field} updated.`);
  showToast("Sandbox write applied");
  renderAll();
}

function rejectProposal(id) {
  const proposal = state.proposals.find((item) => item.id === id);
  if (!proposal) return;
  proposal.status = "rejected";
  addAudit("rejected", `${proposal.id} rejected by human operator.`);
  showToast("Proposal rejected");
  renderAll();
}

function approveAll() {
  state.proposals.filter((proposal) => proposal.status === "waiting").forEach((proposal) => approveProposal(proposal.id));
  showToast("Approve all complete");
}

function reset() {
  state.sheet = structuredClone(baseSheet);
  state.proposals = [];
  state.audit = [];
  addAudit("reset", "Sandbox returned to clean state.");
  renderAll();
}

document.querySelectorAll("nav a").forEach((link) => {
  link.addEventListener("click", () => {
    document.querySelectorAll("nav a").forEach((item) => item.classList.remove("active"));
    link.classList.add("active");
  });
});

byId("scenarioSelect").addEventListener("change", (event) => {
  state.scenarioKey = event.target.value;
  reset();
  renderMessages();
  renderMetrics();
});

byId("generateButton").addEventListener("click", generateProposals);
byId("approveAllButton").addEventListener("click", approveAll);
byId("resetButton").addEventListener("click", reset);

renderScenarios();
renderAll();
