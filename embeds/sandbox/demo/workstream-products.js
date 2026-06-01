const products = {
  speaker: {
    event: {
      name: "Stablecoin Founder Panel",
      date: "2026-06-18",
      topic: "How stablecoins are changing consumer payments",
      format: "45-minute moderated panel",
    },
    speaker: {
      name: "Avery Chen",
      company: "Northstar Wallet",
      bio: "Founder building consumer wallet infrastructure for stablecoin payments.",
      email: "avery@example.com",
    },
    missing: ["Headshot URL", "Speaker title", "Assistant or PR contact", "Approved talking points"],
    questions: [
      ["What did you learn about consumer payments that was not obvious before you started building Northstar Wallet?", "Grounds the panel in founder-specific learning."],
      ["Where are stablecoins already good enough for consumers, and where do they still feel like infrastructure instead of product?", "Separates readiness from optimism."],
      ["What has to be invisible for a consumer wallet to feel trustworthy?", "Connects UX, safety, and infrastructure."],
      ["How do you think about distribution when the user may not care the rail is a stablecoin?", "Moves into go-to-market and adoption."],
      ["What misconception do founders have when building payments products on crypto rails?", "Creates a builder takeaway."],
      ["If we reran this panel in two years, what would need to change for stablecoins to feel normal?", "Sets a concrete adoption bar."],
    ],
    email: {
      subject: "Prep for Stablecoin Founder Panel on 2026-06-18",
      body: "Hi Avery,\n\nExcited to have you join Stablecoin Founder Panel. The session is a 45-minute moderated panel on 'How stablecoins are changing consumer payments.' We will keep the conversation practical for founders and operators.\n\nCould you send over any missing speaker details and a few themes you would be excited to cover?\n\nBest,\nELA Team",
    },
  },
  sponsors: {
    event: {
      name: "Crypto Builder Mixer",
      attendance: 92,
      contacts_captured: 34,
      photos_url: "https://example.com/photos",
    },
    sponsor: {
      company: "BridgeStack",
      contact: "Mina Patel",
      email: "mina@example.com",
    },
    prospects: [
      ["Privy", "Wallet and onboarding infrastructure for crypto apps.", "Sponsor a builder mixer focused on consumer onboarding and wallet UX."],
      ["Bridge", "Stablecoin orchestration and payment infrastructure.", "Meet founders building stablecoin distribution."],
      ["Alchemy", "Developer platform for web3 infrastructure teams.", "Sponsor technical programming for infrastructure builders."],
    ],
  },
  outreach: {
    maintenance: {
      name: "Jordan Lee",
      company: "VaultKit",
      reason: "Last touch was 2026-01-12 and no Gmail activity is summarized after January.",
      angle: "Reconnect around future panel interest and upcoming June programming.",
    },
    candidates: [
      ["Avery Chen", "Northstar Wallet", "crm", "Consumer wallet infrastructure maps to the stablecoin event."],
      ["Jordan Lee", "VaultKit", "crm", "Known VCW relationship with prior interest in panels."],
    ],
    digest: ["1 stale relationship needs follow-up: Jordan Lee at VaultKit.", "2 purpose-driven speaker candidates drafted for June crypto programming."],
  },
};

const explainers = {
  speaker: {
    how: [
      "Input: one event row plus one speaker record.",
      "The product detects missing speaker details, drafts a prep email, creates a calendar prep-block payload, and generates moderator questions.",
      "The operator reviews the draft artifacts before anything becomes a real Gmail draft, calendar hold, or prep document.",
    ],
    has: [
      "Event and speaker context card.",
      "Missing-info checklist.",
      "Six panel questions with why each works.",
      "Briefing email draft.",
      "Calendar prep-block payload in the generated JSON artifact.",
      "Approval boundary: draft-only.",
    ],
    missing: [
      "No live Google Doc template copy yet.",
      "No real Calendar event creation yet.",
      "No real Gmail draft creation from this visual console yet.",
      "No Speaker Prep Sheet tab write yet.",
      "Questions are deterministic demo output, not live Sonnet/Llama generation in this page.",
    ],
  },
  sponsors: {
    how: [
      "Input: sponsor record, event recap metrics, and sponsor-prospecting brief.",
      "The product creates a thank-you draft, renewal prompt, sponsor one-pager payload, and ranked prospect cards.",
      "The operator decides which draft or prospect should move to Gmail, Slides, CRM, or Sheets.",
    ],
    has: [
      "Sponsor follow-up draft.",
      "Event recap metrics: attendance, contacts captured, photos URL.",
      "Slides one-pager payload.",
      "Three ranked sponsor prospects.",
      "Draft outreach angles for top prospects.",
      "Approval boundary: no sending or publishing.",
    ],
    missing: [
      "No live CRM sponsor record sync yet.",
      "No real Slides one-pager generation yet.",
      "No live web research in this visual console yet.",
      "No Gmail draft creation from the browser surface yet.",
      "Prospect list is fixture/demo data, not live researched data.",
    ],
  },
  outreach: {
    how: [
      "Input: CRM relationship records, last-touch context, Gmail/Telegram summaries, and an outreach goal.",
      "The product identifies stale relationships, proposes a reason to reconnect, ranks purpose-fit contacts, and drafts approval-ready messages.",
      "The operator reviews the digest before drafts or CRM updates are created.",
    ],
    has: [
      "Stale relationship card.",
      "Suggested reconnect angle.",
      "Purpose-driven candidate ranking.",
      "Draft email payloads in generated JSON artifact.",
      "Telegram approval digest preview.",
      "Approval boundary: draft-only, no CRM writes.",
    ],
    missing: [
      "No live Relay CRM reader connected in this visual console yet.",
      "No live Gmail-history lookup from this page yet.",
      "No real Telegram digest send yet.",
      "No automatic Gmail draft creation yet.",
      "No web candidate research in this page yet.",
    ],
  },
};

function byId(id) {
  return document.getElementById(id);
}

function productFromQuery() {
  const params = new URLSearchParams(window.location.search);
  return params.get("product") || "";
}

function applyEmbeddedMode() {
  const params = new URLSearchParams(window.location.search);
  const simple = params.get("simple") === "1";
  if (simple) {
    document.body.classList.add("simple");
    if ("scrollRestoration" in history) history.scrollRestoration = "manual";
  }
  const product = productFromQuery();
  if (product) {
    document.querySelectorAll("nav a").forEach((link) => {
      const target = (link.getAttribute("href") || "").replace("#", "");
      link.classList.toggle("active", target === product);
    });
  }
  if (simple) {
    if (window.location.hash) history.replaceState(null, "", window.location.pathname + window.location.search);
    requestAnimationFrame(() => window.scrollTo({ top: 0, left: 0, behavior: "instant" }));
    setTimeout(() => window.scrollTo({ top: 0, left: 0, behavior: "instant" }), 0);
  }
}

function renderExplainer(id, config) {
  byId(id).innerHTML = `
    <article class="explainer primary">
      <span class="tag">how it works</span>
      <h3>What this phase does</h3>
      <ol>${config.how.map((item) => `<li>${item}</li>`).join("")}</ol>
    </article>
    <article class="explainer has">
      <span class="tag good">has now</span>
      <h3>Included in this product demo</h3>
      <ul>${config.has.map((item) => `<li>${item}</li>`).join("")}</ul>
    </article>
    <article class="explainer missing">
      <span class="tag warn">doesn't have yet</span>
      <h3>Still needed for production</h3>
      <ul>${config.missing.map((item) => `<li>${item}</li>`).join("")}</ul>
    </article>
  `;
}

function renderSpeaker() {
  byId("speakerSummary").innerHTML = `
    <span class="tag">speaker prep</span>
    <h3>${products.speaker.event.name}</h3>
    <p><strong>Speaker:</strong> ${products.speaker.speaker.name}, ${products.speaker.speaker.company}</p>
    <p><strong>Topic:</strong> ${products.speaker.event.topic}</p>
    <p><strong>Output:</strong> prep doc payload, missing-info checklist, briefing email draft, calendar prep block, panel questions.</p>
  `;
  byId("missingInfo").innerHTML = products.speaker.missing.map((item) => `<li>${item}</li>`).join("");
  byId("questionGrid").innerHTML = products.speaker.questions
    .map(([question, why]) => `<article class="question"><h3>${question}</h3><p>${why}</p></article>`)
    .join("");
  byId("speakerEmail").innerHTML = `<span class="tag">gmail draft</span><h3>${products.speaker.email.subject}</h3><p>${products.speaker.email.body}</p>`;
  renderExplainer("speakerExplain", explainers.speaker);
}

function renderSponsors() {
  byId("sponsorFollowup").innerHTML = `
    <span class="tag">follow-up</span>
    <h3>${products.sponsors.sponsor.company}</h3>
    <p>Thank-you draft for ${products.sponsors.sponsor.contact} after ${products.sponsors.event.name}.</p>
    <p>Metrics: ${products.sponsors.event.attendance} attendees, ${products.sponsors.event.contacts_captured} contacts captured.</p>
  `;
  byId("onePager").innerHTML = `
    <span class="tag">one-pager payload</span>
    <h3>${products.sponsors.event.name} sponsor recap</h3>
    <p>Slides-ready payload with attendance, contacts captured, photos URL, and next sponsorship angle.</p>
  `;
  byId("prospectGrid").innerHTML = products.sponsors.prospects
    .map(([company, snapshot, angle], index) => `<article class="prospect"><span class="tag">rank ${index + 1}</span><h3>${company}</h3><p>${snapshot}</p><p>${angle}</p></article>`)
    .join("");
  renderExplainer("sponsorExplain", explainers.sponsors);
}

function renderOutreach() {
  byId("maintenanceCard").innerHTML = `
    <span class="tag">relationship maintenance</span>
    <h3>${products.outreach.maintenance.name} · ${products.outreach.maintenance.company}</h3>
    <p>${products.outreach.maintenance.reason}</p>
    <p>${products.outreach.maintenance.angle}</p>
  `;
  byId("digestCard").innerHTML = `<span class="tag">telegram digest</span><h3>Approval summary</h3><ul>${products.outreach.digest.map((item) => `<li>${item}</li>`).join("")}</ul>`;
  byId("outreachGrid").innerHTML = products.outreach.candidates
    .map(([name, company, source, rationale], index) => `<article class="prospect"><span class="tag">${source} · rank ${index + 1}</span><h3>${name}</h3><p>${company}</p><p>${rationale}</p></article>`)
    .join("");
  renderExplainer("outreachExplain", explainers.outreach);
}

function renderApproval() {
  byId("approvalGrid").innerHTML = [
    ["Speaker Prep", "Calendar and Gmail actions are draft-only until reviewed."],
    ["Sponsors", "No sponsor email, CRM update, Sheet row, or Slides one-pager is published automatically."],
    ["Outreach", "Gmail output is draft-only. No CRM write happens without approval."],
  ]
    .map(([title, detail]) => `<article class="approval"><span class="tag">${title}</span><h3>Approval gate</h3><p>${detail}</p></article>`)
    .join("");
}

document.querySelectorAll("nav a").forEach((link) => {
  link.addEventListener("click", () => {
    document.querySelectorAll("nav a").forEach((item) => item.classList.remove("active"));
    link.classList.add("active");
  });
});

renderSpeaker();
renderSponsors();
renderOutreach();
renderApproval();
applyEmbeddedMode();

const requestedProduct = new URLSearchParams(window.location.search).get("product");
if (requestedProduct) {
  const visible = new Set([requestedProduct, "approval"]);
  document.querySelectorAll("main > header, main > section").forEach((section) => {
    const id = section.id || "overview";
    section.style.display = visible.has(id) ? "" : "none";
  });
}
