# nozzle_path.py - Task 5: Nozzle movement
# The nozzle moves in a zigzag across the wall:
#   Pass 1: left to right near the bottom
#   Pass 2: right to left a bit higher
#   Pass 3: left to right higher still
#   ... until it covers the whole wall

import numpy as np
import config


def build_path():
    """Create list of (x, y) positions, one per step."""
    positions = []

    # Evenly spaced Y levels from bottom to top
    y_levels = np.linspace(0.3, 2.7, config.NUM_PASSES)

    for i, y in enumerate(y_levels):
        # X positions across the wall
        xs = np.linspace(-1.8, 1.8, config.STEPS_PER_PASS)

        # Reverse every other pass to make zigzag
        if i % 2 == 1:
            xs = xs[::-1]

        for x in xs:
            positions.append((x, y))

    return positions
