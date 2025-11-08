#!/bin/bash

# ================================
# Colour codes
CYAN='\033[0;36m'
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'  # No Colour
# ================================

# Print ASCII banner in cyan
echo -e "${CYAN}"
cat ./ascii/Passwordsmith.txt
echo -e "${NC}\n"

# Start the Python engine
python3 ./engine.py
