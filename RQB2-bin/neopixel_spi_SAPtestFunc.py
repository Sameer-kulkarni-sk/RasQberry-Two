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
    """Draw SAP logo: S (blue), A (gold), P (green).
    Letters drawn with y-flip (7-y) to match physical quad panel orientation.
    S: col 0-5, A: col 8-13, P: col 16-21
    """

    # --- Letter "S" (SAP Blue) col 0-5, y-flipped ---
    for x in range(0, 6): plotcalc(7, x, SAP_BLUE, pixels, toggle)   # top bar    (drawn at y=7)
    plotcalc(6, 0, SAP_BLUE, pixels, toggle)                           # upper-left (y=6)
    plotcalc(5, 0, SAP_BLUE, pixels, toggle)                           # upper-left (y=5)
    for x in range(0, 6): plotcalc(4, x, SAP_BLUE, pixels, toggle)   # mid bar    (y=4)
    plotcalc(3, 5, SAP_BLUE, pixels, toggle)                           # lower-right (y=3)
    plotcalc(2, 5, SAP_BLUE, pixels, toggle)                           # lower-right (y=2)
    for x in range(0, 6): plotcalc(1, x, SAP_BLUE, pixels, toggle)   # bottom bar  (y=1)
    for x in range(0, 6): plotcalc(0, x, SAP_BLUE, pixels, toggle)   # bottom bar  (y=0)

    # --- Letter "A" (SAP Gold) col 8-13, y-flipped ---
    for x in range(8, 14): plotcalc(7, x, SAP_GOLD, pixels, toggle)   # top bar
    for y in range(0, 7):  plotcalc(y, 8,  SAP_GOLD, pixels, toggle)  # left leg
    for y in range(0, 7):  plotcalc(y, 13, SAP_GOLD, pixels, toggle)  # right leg
    for x in range(9, 13): plotcalc(3, x, SAP_GOLD, pixels, toggle)   # crossbar (y=4 flipped → y=3)

    # --- Letter "P" (SAP Green) col 16-21, y-flipped ---
    for y in range(0, 8):  plotcalc(y, 16, SAP_GREEN, pixels, toggle)  # left leg (full)
    for x in range(17, 22): plotcalc(7, x, SAP_GREEN, pixels, toggle)  # top bar  (y=7)
    for y in range(4, 7):  plotcalc(y, 21, SAP_GREEN, pixels, toggle)  # right side top half
    for x in range(17, 22): plotcalc(3, x, SAP_GREEN, pixels, toggle)  # mid bar  (y=4 flipped → y=3)


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
