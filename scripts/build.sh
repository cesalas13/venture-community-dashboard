#!/bin/bash
# Rebuild the embedded JSON block inside index.html from state.json.
# Run this whenever state.json changes so the file:// fallback stays in sync.
#
# Usage:  ./build.sh
#
set -e
DASH_DIR="$(cd "$(dirname "$0")/.." && pwd)"
STATE="$DASH_DIR/state.json"
INDEX="$DASH_DIR/index.html"

if [ ! -f "$STATE" ]; then
  echo "state.json not found at $STATE"
  exit 1
fi

python3 - <<PY
import re, pathlib
state_path = pathlib.Path("$STATE")
index_path = pathlib.Path("$INDEX")
state_text = state_path.read_text()
index_text = index_path.read_text()
pattern = re.compile(r'(<script type="application/json" id="embedded-state">)(.*?)(</script>)', re.DOTALL)
if not pattern.search(index_text):
    print("ERROR: <script id='embedded-state'> not found in index.html.")
    raise SystemExit(1)
new_text = pattern.sub(lambda m: m.group(1) + "\n" + state_text + "\n" + m.group(3), index_text)
index_path.write_text(new_text)
print(f"[build.sh] embedded {len(state_text)} chars of state.json into index.html")
PY
