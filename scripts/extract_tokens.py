#!/usr/bin/env python3
"""Parse CSS files in a dir and emit tokens.json + tokens.css.
Usage: extract_tokens.py <cssdir>"""
import sys, re, json, glob, collections, os
d = sys.argv[1] if len(sys.argv) > 1 else '.'
css = ""
for f in glob.glob(os.path.join(d,'**','*.css'), recursive=True):
    try: css += open(f, encoding='utf-8', errors='ignore').read() + "\n"
    except Exception: pass
def freq(pat):
    c = collections.Counter(re.findall(pat, css, re.I)); return c.most_common()
colors = freq(r'#[0-9a-f]{3,8}\b|rgba?\([^)]*\)|hsla?\([^)]*\)')
fonts  = freq(r'font-family:\s*([^;{}]+)')
sizes  = freq(r'font-size:\s*([0-9.]+(?:px|rem|em))')
weights= freq(r'font-weight:\s*(\d{3}|bold|normal)')
radius = freq(r'border-radius:\s*([^;{}]+)')
shadow = freq(r'box-shadow:\s*([^;{}]+)')
space  = freq(r'(?:margin|padding|gap):\s*([0-9.]+(?:px|rem|em)[^;{}]*)')
vars_  = dict(re.findall(r'(--[\w-]+)\s*:\s*([^;{}]+)', css))
keyfr  = re.findall(r'@keyframes\s+([\w-]+)', css)
anim   = freq(r'animation(?:-name)?:\s*([^;{}]+)')
trans  = freq(r'transition:\s*([^;{}]+)')
tokens = {
  "colors":[c for c,_ in colors[:40]],
  "fonts":[f.strip() for f,_ in fonts[:10]],
  "fontSizes":[s for s,_ in sizes[:20]],
  "fontWeights":[w for w,_ in weights[:10]],
  "radius":[r for r,_ in radius[:12]],
  "shadow":[s.strip() for s,_ in shadow[:12]],
  "spacing":[s for s,_ in space[:24]],
  "cssVars":vars_,
  "keyframes":sorted(set(keyfr)),
  "animations":[a.strip() for a,_ in anim[:20]],
  "transitions":[t.strip() for t,_ in trans[:20]],
}
open('tokens.json','w').write(json.dumps(tokens, indent=2, ensure_ascii=False))
with open('tokens.css','w') as out:
    out.write(":root{\n")
    for k,v in vars_.items(): out.write(f"  {k}: {v.strip()};\n")
    for i,c in enumerate(tokens['colors']): out.write(f"  --color-{i+1}: {c};\n")
    out.write("}\n")
print("wrote tokens.json + tokens.css")
print(f"colors={len(tokens['colors'])} fonts={len(tokens['fonts'])} keyframes={len(tokens['keyframes'])} vars={len(vars_)}")
