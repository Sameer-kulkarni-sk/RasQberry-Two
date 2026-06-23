#!/bin/bash
#
# rq_sap_learning_auto.sh - SAP Quantum Learning App Launcher
#
# Clones rasqberry-sap-demo on first run, installs Node.js deps if needed,
# starts the React dev server, waits for it to be ready, then opens Chromium.
#

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "${SCRIPT_DIR}/rq_common.sh"

load_rqb2_env

DEMO_NAME="rasqberry-sap-demo"
REPO_URL="https://github.com/Sameer-kulkarni-sk/rasqberry-sap-demo.git"
DEMO_DIR=$(get_demo_dir "$DEMO_NAME")
MARKER="$DEMO_DIR/package.json"
PORT=3000
URL="http://localhost:$PORT"

if [ ! -f "$MARKER" ]; then
    info "SAP Quantum Learning not found. Cloning..."
    clone_demo "$REPO_URL" "$DEMO_DIR"
fi

if ! command -v node >/dev/null 2>&1; then
    info "Node.js not found. Installing..."
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi

if [ ! -d "$DEMO_DIR/node_modules" ]; then
    info "Installing Node.js dependencies (this may take a few minutes)..."
    cd "$DEMO_DIR"
    run_as_user npm install --prefix "$DEMO_DIR"
fi

info "Starting SAP Quantum Learning server on port $PORT..."
cd "$DEMO_DIR"

# Kill any existing server on this port
fuser -k ${PORT}/tcp 2>/dev/null || true

# Start npm as the actual user in the background
USER_NAME=$(get_user_name)
sudo -u "$USER_NAME" -H bash -c "cd '$DEMO_DIR' && npm start" &
SERVER_PID=$!

# Clean up server on exit
trap "kill $SERVER_PID 2>/dev/null || true; fuser -k ${PORT}/tcp 2>/dev/null || true" EXIT INT TERM

info "Waiting for server to be ready (this may take up to 60 seconds on first run)..."
for i in $(seq 1 30); do
    if curl -s "$URL" >/dev/null 2>&1; then
        info "Server ready."
        break
    fi
    sleep 2
done

export DISPLAY="${DISPLAY:-:0}"
open_browser "$URL"

# Keep script alive so the terminal stays open and server keeps running
info "SAP Quantum Learning is running. Close this terminal to stop the server."
wait "$SERVER_PID"
