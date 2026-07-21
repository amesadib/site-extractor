---
name: site-extractor
description: >-
  Extract a live website's full front-end — HTML, CSS, JS, fonts, images, design
  tokens (colors, typography, spacing, shadows), and graphic motion (CSS keyframes,
  transitions, GSAP/Framer Motion/Lottie/ScrollTrigger) — then rebuild it inside the
  user's own project (plain HTML/CSS or React + Tailwind). Use when the user says
  "clone this site", "extract this design", "pull the code/animations from this URL",
  "rebuild this site in my project", "copy this landing page", or provides a URL and
  asks to reproduce its look, layout, or motion. Token-efficient: fetches static
  assets in the sandbox and reads only computed design data, not full DOM dumps.
metadata:
  version: 1.0.0
  author: cowork/bob
  category: web-frontend
  requires: [bash, wget, node, python3]
---

# Site Extractor

Turn any public web page into reusable front-end code inside the user's project.
Work in phases. Never skip Phase 0 (legal) or Phase 5 (adapt, don't blind-copy).

## Phase 0 — Scope & legal gate (mandatory, <60s)

- Confirm the URL and what to extract: full page, one section, only the design
  system, or only the animations.
- A site's HTML/CSS/JS, brand assets, logos, copy, and images are usually
  copyrighted/trademarked. Only reproduce sites the user owns or has permission
  for, or extract for private learning. Do NOT copy logos, brand names, or
  proprietary copy into a public/commercial project. Rebuild structure and
  technique, replace brand assets with the user's own.
- State this once, briefly, then proceed.

## Phase 1 — Capture the rendered page (source of truth)

Modern sites are JS-rendered, so raw HTML is not enough. Use the browser to get
the *computed* result, then the sandbox for the *raw assets*.

Browser (Claude in Chrome MCP), do all of these:
- `navigate` to the URL, wait for load.
- `read_page` for the rendered DOM + text structure.
- `read_network_requests` to list every CSS, JS, font, image, and XHR asset URL.
- `javascript_tool` to dump the design system directly from the live page
  (see `scripts/dump_design.js`). This returns compact JSON, not a huge DOM.

## Phase 2 — Pull the raw assets (sandbox, cheap)

Run `scripts/fetch_site.sh <URL> <outdir>`. It mirrors HTML, CSS, JS, fonts, and
images with wget, then lists what it got. This runs in the Linux sandbox and costs
no model tokens for the download itself.

## Phase 3 — Extract design tokens

Run `scripts/extract_tokens.py <cssdir>` to parse every stylesheet and emit:
- Color palette (grouped, deduped, with usage counts)
- Typography scale (font families, sizes, weights, line-heights)
- Spacing / radius / shadow scales
- CSS custom properties (`--vars`) already defined by the site
Output is a single `tokens.json` + a `tokens.css` you can drop into a project.

## Phase 4 — Extract motion & graphics

See `references/motion-extraction.md`. In short:
- Grep CSS for `@keyframes`, `transition`, `animation`, `transform`, `will-change`.
- Detect JS motion libs from network assets: GSAP, ScrollTrigger, Framer Motion,
  Lottie (`.json` bodymovin), Three.js, Rive, Locomotive/Lenis smooth-scroll,
  Swiper, particles.
- For Lottie, download the animation JSON — it is fully portable.
- For GSAP/scroll effects, capture the trigger, easing, duration, and stagger,
  and reproduce with the same lib in the target project.
- Record the exact easing curves and durations; they are what make it feel right.

## Phase 5 — Rebuild in the user's project (adapt, don't dump)

- Ask/confirm target stack: plain HTML+CSS, or React + Tailwind, or Next.js.
- Map extracted tokens to the target (Tailwind `theme.extend`, or `:root` vars).
- Recreate layout section by section using semantic markup; do not paste minified
  vendor blobs. Keep it clean and maintainable.
- Reinstall motion with the same library + captured easing/duration values.
- Swap all brand assets for the user's own (Phase 0).
- Deliver files into the user's project folder and list what maps to what.

## Token discipline

- Never paste a full rendered DOM or a minified bundle into context.
- Prefer the compact JSON from `dump_design.js` and `tokens.json`.
- Read vendor JS only to identify the lib and its config, not line by line.
- Do heavy fetching/parsing in the sandbox; bring back summaries only.

## Quality checklist

- [ ] Layout matches at desktop + mobile breakpoints
- [ ] Fonts + fallbacks correct
- [ ] Color/spacing/shadow tokens mapped, not hard-coded ad hoc
- [ ] Key animations reproduced with correct easing + timing
- [ ] Brand assets replaced; no trademarked material copied
- [ ] Code is clean and lives in the user's project structure
