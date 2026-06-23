# SPDX-FileCopyrightText: 2024 RasQberry Contributors
# SPDX-License-Identifier: MIT
# SAP LED Demo for RasQberry - follows IBM LED demo style exactly

import time
import sys
import select
from rq_led_utils import get_led_config, create_neopixel_strip, chunked_show, map_xy_to_pixel

# Load configuration from environment file
config = get_led_config()

# SAP brand colors  (R, G, B)
SAP_BLUE   = (0,  58, 108)   # SAP Dark Blue  #003A6C
SAP_GOLD   = (240, 171,  0)  # SAP Gold       #F0AB00
SAP_GREEN  = (30, 160,  98)  # SAP Green      #1EA062

DELAY = 5

# Create LED strip (auto-detects Pi4 PWM or Pi5 PIO)
pixels = create_neopixel_strip(
    config['led_count'],
    config['pixel_order'],
    brightness=config['led_default_brightness']
)


def plotcalc(y, x, color, pixels, rainbow):
    """
    Calculate pixel index using environment-configured layout.
    Mirrors IBM demo plotcalc exactly — rainbow rows use SAP palette.
    """
    i = map_xy_to_pixel(x, y)
    if i is None:
        return

    if rainbow:
        if y == 7: color = (251, 128, 191)  # pink
        if y == 6: color = (250,   1,   0)  # red
        if y == 5: color = (249, 131,  31)  # orange
        if y == 4: color = (248, 223,   8)  # yellow
        if y == 3: color = (  2, 162,   4)  # green
        if y == 2: color = (  0, 196, 173)  # turquoise
        if y == 1: color = (  0,  65, 183)  # blue
        if y == 0: color = (131,  32, 158)  # purple

    pixels[i] = color


def dosap(toggle):
    """Draw SAP logo: S (blue), A (gold), P (green)."""

    # --- Letter "S" (SAP Blue) ---
    # Top bar
    for x in range(1, 6): plotcalc(7, x, SAP_BLUE, pixels, toggle)
    # Upper left vertical
    plotcalc(6, 1, SAP_BLUE, pixels, toggle)
    # Middle bar
    for x in range(1, 6): plotcalc(4, x, SAP_BLUE, pixels, toggle)
    plotcalc(5, 1, SAP_BLUE, pixels, toggle)
    # Lower right vertical
    plotcalc(3, 5, SAP_BLUE, pixels, toggle)
    # Bottom bar
    for x in range(1, 6): plotcalc(0, x, SAP_BLUE, pixels, toggle)
    plotcalc(1, 5, SAP_BLUE, pixels, toggle)
    # Corner fills
    plotcalc(6, 5, SAP_BLUE, pixels, toggle)
    plotcalc(2, 1, SAP_BLUE, pixels, toggle)

    # --- Letter "A" (SAP Gold) ---
    # Left vertical
    for y in range(0, 8): plotcalc(y, 9,  SAP_GOLD, pixels, toggle)
    # Right vertical
    for y in range(0, 8): plotcalc(y, 13, SAP_GOLD, pixels, toggle)
    # Top bar
    plotcalc(7, 10, SAP_GOLD, pixels, toggle)
    plotcalc(7, 11, SAP_GOLD, pixels, toggle)
    plotcalc(7, 12, SAP_GOLD, pixels, toggle)
    # Middle bar
    plotcalc(4, 10, SAP_GOLD, pixels, toggle)
    plotcalc(4, 11, SAP_GOLD, pixels, toggle)
    plotcalc(4, 12, SAP_GOLD, pixels, toggle)

    # --- Letter "P" (SAP Green) ---
    # Left vertical (full height)
    for y in range(0, 8): plotcalc(y, 17, SAP_GREEN, pixels, toggle)
    # Top bar
    plotcalc(7, 18, SAP_GREEN, pixels, toggle)
    plotcalc(7, 19, SAP_GREEN, pixels, toggle)
    plotcalc(7, 20, SAP_GREEN, pixels, toggle)
    # Middle bar
    plotcalc(4, 18, SAP_GREEN, pixels, toggle)
    plotcalc(4, 19, SAP_GREEN, pixels, toggle)
    plotcalc(4, 20, SAP_GREEN, pixels, toggle)
    # Right vertical (upper half only)
    plotcalc(6, 21, SAP_GREEN, pixels, toggle)
    plotcalc(5, 21, SAP_GREEN, pixels, toggle)


print("Press Enter to stop...")
print()

try:
    while True:
        dosap(0)                # Solid SAP brand colors
        chunked_show(pixels)
        time.sleep(DELAY)
        dosap(1)                # Rainbow gradient
        chunked_show(pixels)
        time.sleep(DELAY)

        # Non-blocking Enter key check
        if select.select([sys.stdin], [], [], 0)[0]:
            sys.stdin.readline()
            print("\nStopping demo...")
            break
except KeyboardInterrupt:
    print("\nStopping demo...")

# Turn off all LEDs
pixels.fill((0, 0, 0))
chunked_show(pixels)
