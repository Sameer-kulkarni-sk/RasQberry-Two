#!/bin/bash
set -uo pipefail

################################################################################
# rq_sap_led_auto.sh - RasQberry LED SAP Demo Launcher
#
# Description:
#   Simple wrapper to run the SAP-themed LED demonstration
#   Displays SAP logo and animations on LED strip
################################################################################

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "${SCRIPT_DIR}/rq_common.sh"

# Ensure running as root (PWM/PIO drivers require GPIO access)
ensure_root "$@"

# Load environment and verify required variables
load_rqb2_env
verify_env_vars USER_HOME REPO BIN_DIR STD_VENV

# Check multiple possible locations for the script
LED_SCRIPT=""
for location in "$BIN_DIR/neopixel_spi_SAPtestFunc.py" \
                "/usr/bin/neopixel_spi_SAPtestFunc.py" \
                "$USER_HOME/$REPO/RQB2-bin/neopixel_spi_SAPtestFunc.py"; do
    if [ -f "$location" ]; then
        LED_SCRIPT="$location"
        break
    fi
done

[ -n "$LED_SCRIPT" ] || die "LED demo script not found. Searched:\n  - $BIN_DIR/neopixel_spi_SAPtestFunc.py\n  - /usr/bin/neopixel_spi_SAPtestFunc.py\n  - $USER_HOME/$REPO/RQB2-bin/neopixel_spi_SAPtestFunc.py"

info "Starting LED SAP Demo..."
debug "Script location: $LED_SCRIPT"
echo

# Activate virtual environment if available
activate_venv || warn "Virtual environment not available, continuing anyway..."

# Run the script
python3 "$LED_SCRIPT"

echo
read -p "Press Enter to close this window..."
