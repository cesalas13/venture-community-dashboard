const initialState = {
  issue: {
    number: "073",
    type: "Founder Chat",
    target: "Northstar Wallet Founder Chat",
    lumaLink: "https://lu.ma/demo-northstar",
    status: "draft generated",
    docUrl: "https://docs.google.com/demo/vcw-073-northstar",
    context:
      "Founder Chat with Avery Chen of Northstar Wallet. Topic: stablecoin consumer payments. Northstar has 3.1M wallets created, $1B processed, and a $20M Series A. Event is June 18, 5 PM PT, webinar format.",
    hookAngle: "Stablecoin consumer payments are moving from infrastructure to product.",
    mustInclude: "3.1M wallets, $1B processed, $20M Series A",
    mustNotInclude: "featuring, excited to announce, actually",
  },
  rules: [
    {
      label: "Opening sentence",
      value: "Lead with the company, speaker, metric, or hard market problem. Never open with Operator or the date.",
      source: "Elements tab",
    },
    {
      label: "Founder Chat format",
      value: "Use The Problem, The Solution, The Market, Meet the Founder, then Q&A CTA.",
      source: "Issue #066 Belo benchmark",
    },
    {
      label: "Banned words",
      value: "featuring, excited to announce, game-changing, world class, actually, come prepared to share",
      source: "Elements tab",
    },
    {
      label: "Luma structure",
      value: "One opener, credibility hook, Here’s what to expect, Who / Where / When / What, VCW curation closer, Request access below.",
      source: "Luma description rules",
    },
    {
      label: "LinkedIn",
      value: "45 to 80 words. Never start with I or We. Max 2 hashtags at the end.",
      source: "Social voice",
    },
    {
      label: "Direct email",
      value: "Subject 6 to 12 words. Body 50 to 90 words.",
      source: "Social voice",
    },
  ],
  feedback: [
    {
      who: "Operator",
      thought: "The hook was too long on the last issue. Get to the point faster.",
      status: "pending",
      extracted: "Hook must land in the first sentence.",
    },
    {
      who: "Operator",
      thought: "Never use the word featuring.",
      status: "pending",
      extracted: "Add featuring to banned words.",
    },
    {
      who: "Team",
      thought: "The What to Expect vibe line should be one sentence max.",
      status: "pending",
      extracted: "Vibe line must stay to one sentence.",
    },
  ],
  links: [
    {
      phrase: "Avery Chen",
      type: "LinkedIn",
      url: "",
      status: "find it",
    },
    {
      phrase: "Northstar Wallet",
      type: "Website",
      url: "https://northstar.example",
      status: "ready",
    },
    {
      phrase: "Register here",
      type: "Luma",
      url: "https://lu.ma/demo-northstar",
      status: "ready",
    },
  ],
  log: [
    {
      time: "May 4, 2026 10:12 PM",
      action: "Generated draft",
      detail: "Issue 073, Founder Chat, estimated $0.042 local sandbox cost display.",
    },
    {
      time: "May 4, 2026 10:13 PM",
      action: "Hyperlinks queued",
      detail: "3 link targets found, 1 needs manual URL lookup.",
    },
  ],
};

const state = structuredClone(initialState);

function byId(id) {
  return document.getElementById(id);
}

function toast(message) {
  const node = byId("toast");
  node.textContent = message;
  node.classList.add("visible");
  setTimeout(() => node.classList.remove("visible"), 1600);
}

function blockers() {
  const items = [];
  if (!state.issue.lumaLink) items.push(["blocked", "Missing Luma link", "Generate tab row B17 needs a registration URL."]);
  if (state.links.some((link) => link.status !== "ready")) items.push(["blocked", "Unresolved hyperlinks", "Hyperlinks tab has phrases that still need URLs."]);
  if (state.feedback.some((item) => item.status === "pending")) items.push(["warn", "Feedback not processed", "Feedback inbox has raw notes that should become rules."]);
  if (state.issue.mustNotInclude.includes("featuring")) items.push(["good", "Banned phrase guard active", "Must NOT Include field is blocking common old-voice phrasing."]);
  if (!items.some((item) => item[0] === "blocked")) items.push(["good", "Promotion can move to human review", "All hard blockers cleared."]);
  return items;
}

function renderMetrics() {
  const pendingLinks = state.links.filter((link) => link.status !== "ready").length;
  const pendingFeedback = state.feedback.filter((item) => item.status === "pending").length;
  const hardBlocks = blockers().filter((item) => item[0] === "blocked").length;
  byId("metrics").innerHTML = [
    ["Product", "Newsletter / Content"],
    ["Issue", `#${state.issue.number}`],
    ["Status", state.issue.status],
    ["Hard blockers", hardBlocks],
    ["Links pending", pendingLinks],
    ["Feedback pending", pendingFeedback],
  ].map(([label, value]) => `<article class="metric"><span>${label}</span><strong>${value}</strong></article>`).join("");
}

function renderGenerate() {
  byId("issueCard").innerHTML = `
    <h3>Issue</h3>
    <dl>
      <div><dt>Issue Number</dt><dd>#${state.issue.number}</dd></div>
      <div><dt>Issue Type</dt><dd>${state.issue.type}</dd></div>
      <div><dt>Target</dt><dd>${state.issue.target}</dd></div>
      <div><dt>Draft Doc</dt><dd><code>${state.issue.docUrl}</code></dd></div>
    </dl>
  `;

  byId("contextCard").innerHTML = `
    <h3>Context Paste</h3>
    <p>${state.issue.context}</p>
    <dl>
      <div><dt>Luma Link</dt><dd><code>${state.issue.lumaLink}</code></dd></div>
    </dl>
  `;

  byId("overrideCard").innerHTML = `
    <h3>Overrides</h3>
    <dl>
      <div><dt>Hook Angle</dt><dd>${state.issue.hookAngle}</dd></div>
      <div><dt>Must Include</dt><dd>${state.issue.mustInclude}</dd></div>
      <div><dt>Must NOT Include</dt><dd>${state.issue.mustNotInclude}</dd></div>
    </dl>
  `;
}

function renderReadiness() {
  byId("readinessGrid").innerHTML = blockers().map(([status, title, detail]) => `
    <article class="readiness-card">
      <span class="status ${status}">${status === "blocked" ? "blocked" : status === "warn" ? "needs review" : "ready"}</span>
      <h3>${title}</h3>
      <p>${detail}</p>
    </article>
  `).join("");
}

function renderRules() {
  byId("rulesGrid").innerHTML = state.rules.map((rule) => `
    <article class="rule-card">
      <span class="status">${rule.source}</span>
      <h3>${rule.label}</h3>
      <p>${rule.value}</p>
    </article>
  `).join("");
}

function renderFeedback() {
  byId("feedbackGrid").innerHTML = state.feedback.map((item) => `
    <article class="feedback-card">
      <span class="status ${item.status === "pending" ? "warn" : ""}">${item.status}</span>
      <h3>${item.who}</h3>
      <p>${item.thought}</p>
      <p><strong>Extracted rule:</strong> ${item.extracted}</p>
    </article>
  `).join("");
}

function renderLinks() {
  byId("linksBody").innerHTML = state.links.map((link) => `
    <tr>
      <td>${link.phrase}</td>
      <td>${link.type}</td>
      <td>${link.url ? `<code>${link.url}</code>` : "<em>missing</em>"}</td>
      <td><span class="status ${link.status === "ready" ? "" : "warn"}">${link.status}</span></td>
    </tr>
  `).join("");
}

function renderLog() {
  byId("logStack").innerHTML = state.log.map((item) => `
    <article class="log-item">
      <span class="status">${item.time}</span>
      <h3>${item.action}</h3>
      <p>${item.detail}</p>
    </article>
  `).join("");
}

function renderAll() {
  renderMetrics();
  renderGenerate();
  renderReadiness();
  renderRules();
  renderFeedback();
  renderLinks();
  renderLog();
}

function addLog(action, detail) {
  state.log.unshift({
    time: new Date().toLocaleString(),
    action,
    detail,
  });
}

byId("simulateButton").addEventListener("click", () => {
  state.issue.status = "draft generated";
  addLog("Simulated Generate Draft", "Created fake title options, Luma description, LinkedIn post, direct email, and hyperlink queue.");
  toast("Draft simulation complete");
  renderAll();
});

byId("resolveLinksButton").addEventListener("click", () => {
  state.links = state.links.map((link) => link.status === "ready" ? link : {
    ...link,
    url: "https://linkedin.example/avery-chen",
    status: "ready",
  });
  addLog("Resolved hyperlinks", "Filled missing LinkedIn URL in the fake Hyperlinks tab.");
  toast("Links resolved");
  renderAll();
});

byId("learnButton").addEventListener("click", () => {
  state.feedback = state.feedback.map((item) => ({ ...item, status: "done" }));
  addLog("Processed Feedback Inbox", "Converted 3 raw notes into reusable Elements rules.");
  toast("Feedback processed");
  renderAll();
});

byId("resetButton").addEventListener("click", () => {
  Object.assign(state, structuredClone(initialState));
  toast("Newsletter sandbox reset");
  renderAll();
});

document.querySelectorAll("nav a").forEach((link) => {
  link.addEventListener("click", () => {
    document.querySelectorAll("nav a").forEach((item) => item.classList.remove("active"));
    link.classList.add("active");
  });
});

renderAll();
