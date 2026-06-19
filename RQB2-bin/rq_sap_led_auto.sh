#!/bin/bash
#
# rq_sap_led_auto.sh - SAP Quantum LED Demo Launcher
#
# Clones SAP-IBM-Quantum-LED on first run, then executes the main LED script.
# Requires root for GPIO/NeoPixel hardware access.
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "${SCRIPT_DIR}/rq_common.sh"

load_rqb2_env

DEMO_NAME="SAP-IBM-Quantum-LED"
REPO_URL="https://github.com/Sameer-kulkarni-sk/SAP-IBM-Quantum-LED.git"
DEMO_DIR=$(get_demo_dir "$DEMO_NAME")
MARKER="$DEMO_DIR/scripts/deploy_to_rasqberry.sh"
MAIN_SCRIPT="$DEMO_DIR/src/sap_quantum_led_demo.py"

if [ ! -f "$MARKER" ]; then
    info "SAP Quantum LED not found. Cloning..."
    clone_demo "$REPO_URL" "$DEMO_DIR"
fi

require_command python3

ensure_root "$@"

info "Launching SAP Quantum LED..."
cd "$DEMO_DIR"
export PYTHONPATH="/usr/bin:${PYTHONPATH:-}"
exec python3 "$MAIN_SCRIPT" "$@"
