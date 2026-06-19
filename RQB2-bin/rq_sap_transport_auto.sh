#!/bin/bash
#
# rq_sap_transport_auto.sh - SAP Quantum Transportation Optimizer Launcher
#
# Clones SAP-Quantum-Transportation-Optimizer on first run, installs pip
# dependencies, then runs the optimizer CLI in a terminal.
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "${SCRIPT_DIR}/rq_common.sh"

load_rqb2_env

DEMO_NAME="sap-transport"
REPO_URL="https://github.com/Sameer-kulkarni-sk/SAP-Quantum-Transportation-Optimizer.git"
DEMO_DIR=$(get_demo_dir "$DEMO_NAME")
MARKER="$DEMO_DIR/src/main.py"
VENV_DIR="$DEMO_DIR/.venv"

if [ ! -f "$MARKER" ]; then
    info "SAP Transport Optimizer not found. Cloning..."
    clone_demo "$REPO_URL" "$DEMO_DIR"
fi

require_command python3

if [ ! -d "$VENV_DIR" ]; then
    info "Creating virtual environment..."
    run_as_user python3 -m venv "$VENV_DIR"
fi

if [ -f "$DEMO_DIR/requirements.txt" ] && [ ! -f "$DEMO_DIR/.deps_installed" ]; then
    info "Installing Python dependencies..."
    run_as_user "$VENV_DIR/bin/pip" install -r "$DEMO_DIR/requirements.txt"
    touch "$DEMO_DIR/.deps_installed"
fi

info "Launching SAP Quantum Transportation Optimizer GUI..."
cd "$DEMO_DIR"
export DISPLAY="${DISPLAY:-:0}"
run_as_user "$VENV_DIR/bin/python3" src/gui_main.py "$@"
