#!/usr/bin/env bash
set -e

echo "Installing Passwordsmith..."

# Check for python3
if command -v python3 >/dev/null 2>&1; then
    PY=python3
elif command -v python >/dev/null 2>&1; then
    # sometimes `python` is python3
    PY=python
else
    echo "ERROR: Python3 is required. Install python3 and retry."
    exit 1
fi

# Check python version
VER=$($PY -c 'import sys; print(sys.version_info[:2])')
if [[ $VER != *"(3,"* && $VER != *"3"* ]]; then
    echo "WARNING: Make sure your default python is Python 3. Running with $PY"
fi

# Make scripts executable
chmod +x Passwordsmith.sh

# Create wordlists folder
mkdir -p wordlists

cat <<'EOF'
Install complete.
Run the tool:
  bash passwordsmith.sh
EOF

exit 0
