#!/usr/bin/env bash
set -e

# Quick smoke test for Passwordsmith engine
# This feeds answers to engine.py non-interactively and generates the minimum recommended 10,000 lines.
#
# If you want to abort while running: press Ctrl+C

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$SCRIPT_DIR"

echo "Running Passwordsmith smoke test from: $SCRIPT_DIR"
echo "Make sure Python3 is installed. This test will generate 10,000 lines (min)."

# Run engine.py with pre-filled answers
python3 engine.py <<'EOF'
I understand
10000
TestFirst
TestLast
nick1,nick2
2009
2018
fujairah
testuser123
rex
anna
1234
pizza,sslc,snake
12345,1230,55555

Y
Y
Y
Y
EOF

# After the script finishes, show the output file created (most recent)
OUT_DIR="$SCRIPT_DIR/wordlists"
echo
echo "Files in wordlists/:"
ls -1 -- "$OUT_DIR" | tail -n 10

LATEST=$(ls -1t "$OUT_DIR" | head -n1)
echo
echo "Latest output: $OUT_DIR/$LATEST"
echo "First 20 lines of the generated wordlist:"
head -n 20 "$OUT_DIR/$LATEST" || true

echo
echo "Smoke test finished."
