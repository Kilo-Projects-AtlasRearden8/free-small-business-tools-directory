# STATUS — Freebies Directory

## What was built

A static "Freebies" directory of free small-business tools: invoicing,
bookkeeping, scheduling, and contracts. It ships as:

- `index.html` — self-contained static HTML site with client-side search
  (keyword + category filter), no build step, no server required. Opens directly
  in a browser from the `file://` scheme or any static host.
- `tools.json` — canonical machine-readable listing (19 tools across 4
  categories). The same data is embedded in `index.html` so the site works
  without fetching external files.
- `css/style.css` — warm, polished, responsive styles.
- `js/app.js` — vanilla JS client-side search/render (no dependencies).
- `README.md` — Markdown mirror of the directory (cost, platform, steps,
  official link per listing), with Asdale Dynamics, LLC credit.
- `LICENSE` — MIT License, copyright line exactly
  `Copyright (c) 2026 Asdale Dynamics, LLC`.
- `STATUS.md` — this file.

## Contents

19 free-tool listings:

- Invoicing (5): Wave Invoicing, Zoho Invoice, Invoice Ninja, Square Invoices,
  PayPal Invoicing
- Bookkeeping (5): Wave Accounting, GnuCash, Manager.io, Google Sheets,
  NCH Express Accounts
- Scheduling (4): Calendly, Setmore, Google Calendar, SimplyMeet
- Contracts (5): Dropbox Sign, PandaDoc, Jotform Sign, SignWell, Signaturely

Each listing includes cost, platform, steps to get started, and official link.
No affiliate links; every link points to the tool's official website.

## How to run

Open `index.html` in any modern browser (double-click, or `python3 -m http.server`
in this folder and visit `http://localhost:8000/`). Nothing to install, no API
keys, no secrets, no personal data in any file.

## Verification results

- `tools.json` parses as valid JSON: 19 tools, 4 categories
- Embedded JSON in `index.html` is byte-identical to `tools.json`
- LICENSE contains the exact line `Copyright (c) 2026 Asdale Dynamics, LLC`
- All 19 official links use `https://`; none contain affiliate/referral/UTM
  parameters (`ref=`, `affiliate`, `utm_`, `partner=`, `tracking=`)
- Every listing has all required fields: cost, platform, steps, official link
- README.md credits Asdale Dynamics, LLC
- Site serves over HTTP with status 200; CSS and JS load successfully
- Client-side search logic verified with node: keyword search, category filter,
  combined search, and empty results all behave correctly

## Known gaps

- Pricing/free-tier limits change over time; each listing notes where fees may
  apply, but users should confirm on the official site before signing up.
- Not tested in a headless browser; verified via HTTP serve, JSON parsing, and
  node replication of the search logic instead.
- Listings are educational only and are not legal, tax, or medical advice.
- No GitHub Actions or CI workflows were added (by design).
