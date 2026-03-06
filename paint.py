# paint.py - Task 3: Paint accumulation
# A grid tracks how much paint is on each part of the wall.
# Each spray step adds paint where hits landed.
# Over time, paint builds up from 0 (empty) to 1 (fully painted).

import numpy as np
from pxr import Gf
import config


class PaintGrid:
    def __init__(self):
        """Start with empty wall — no paint anywhere."""
        n = config.GRID_RES
        self.grid = np.zeros((n, n), dtype=np.float32)

    def add_paint(self, hit_uvs):
        """Deposit paint where spray hit the wall."""
        if len(hit_uvs) == 0:
            return

        n = config.GRID_RES

        # UV to grid cell: u goes left-right, v goes bottom-top
        col = np.clip((hit_uvs[:, 0] * n).astype(int), 0, n - 1)
        row = np.clip(((1.0 - hit_uvs[:, 1]) * n).astype(int), 0, n - 1)

        # Each hit adds a small amount of paint
        np.add.at(self.grid, (row, col), config.PAINT_AMOUNT)

        # Cap at 1.0 — can't have more than fully painted
        np.clip(self.grid, 0.0, 1.0, out=self.grid)

    def get_coverage(self):
        """Percentage of wall that has paint on it."""
        return float(np.mean(self.grid > 0.01)) * 100

    def get_face_colors(self):
        """Convert paint grid to colors for each wall face.
        No paint = gray wall, full paint = red."""
        n = config.GRID_RES
        bg = np.array(config.WALL_COLOR)
        paint = np.array(config.PAINT_COLOR)

        colors = []
        for row in range(n):
            for col in range(n):
                amount = self.grid[n - 1 - row, col]
                c = bg * (1.0 - amount) + paint * amount
                colors.append(Gf.Vec3f(c[0], c[1], c[2]))
        return colors
