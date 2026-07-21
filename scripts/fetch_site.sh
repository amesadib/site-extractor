#!/usr/bin/env bash
# Usage: fetch_site.sh <URL> <outdir>
set -e
URL="$1"; OUT="${2:-site_dump}"
mkdir -p "$OUT"; cd "$OUT"
echo "Mirroring $URL ..."
wget -e robots=off -nv -H -k -p -E \
  --span-hosts --no-parent --level=1 \
  --user-agent="Mozilla/5.0 (compatible; SiteExtractor/1.0)" \
  "$URL" 2>&1 | tail -5 || true
echo "--- assets pulled ---"
find . -type f | sed 's|^\./||' | sort
echo "--- CSS files ---";  find . -iname '*.css' | sort
echo "--- JS files ---";   find . -iname '*.js'  | sort
echo "--- fonts ---";      find . -iregex '.*\.\(woff2?\|ttf\|otf\|eot\)' | sort
echo "--- Lottie json (bodymovin) ---"; grep -rls '"v":".*","fr"' . 2>/dev/null | head
