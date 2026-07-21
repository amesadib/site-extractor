# site-extractor

A strong Claude Code / Agent skill that extracts a live website's front-end —
HTML, CSS, JS, fonts, images, **design tokens** (colors, typography, spacing,
shadows), and **graphic motion** (CSS keyframes, GSAP, ScrollTrigger, Framer
Motion, Lottie, Three.js) — then rebuilds it inside your own project (plain
HTML/CSS or React + Tailwind).

Token-efficient: heavy downloading and CSS parsing run in a sandbox/shell; only
compact JSON summaries go back to the model.

## Install (Claude Code)
```bash
git clone https://github.com/<your-username>/site-extractor /tmp/se
mkdir -p ~/.claude/skills
cp -r /tmp/se ~/.claude/skills/site-extractor   # or: cp -r /tmp/se/skills/site-extractor ~/.claude/skills/
```
Restart Claude Code, then check with `/skills`.

## Usage
Give Claude a URL, e.g. *"use site-extractor to pull the hero + scroll motion of
https://example.com into my React+Tailwind project"*.

## Files
- `SKILL.md` — the phased workflow
- `scripts/dump_design.js` — run in-browser to dump the live design system as JSON
- `scripts/fetch_site.sh` — mirror raw assets with wget
- `scripts/extract_tokens.py` — parse CSS into tokens.json + tokens.css
- `references/motion-extraction.md` — detect and port every motion type

## Legal
Only reproduce sites you own or have permission for, or for private learning.
Do not copy logos, brand names, or proprietary copy into public/commercial work.

## License
MIT
