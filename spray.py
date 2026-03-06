# spray.py - Task 2: Spray simulation
# The spray forms a TRIANGULAR FAN pattern:
#
#   Seen from above (top view):
#
#        nozzle
#          *
#         /|\
#        / | \
#       /  |  \
#      /   |   \
#     -----+-----   <-- wall
#
#   The fan is wide horizontally and has some vertical spread.
#   Configurable: FAN_ANGLE (width), SPRAY_RANGE, SPRAY_DENSITY

import warp as wp
import numpy as np
import config

wp.init()

@wp.kernel
def shoot_spray(
    nozzle_pos: wp.vec3,
    fan_angle: float,
    seed: int,
    origins: wp.array(dtype=wp.vec3),
    directions: wp.array(dtype=wp.vec3),
):
    """Generate spray rays in a triangular fan pattern.
    Horizontal spread = full fan angle.
    Vertical spread = half of fan angle (fan is wider than tall)."""
    i = wp.tid()
    rng = wp.rand_init(seed, i)

    # Horizontal: full fan width
    angle_h = (wp.randf(rng) * 2.0 - 1.0) * fan_angle

    # Vertical: half the fan width (triangular fan is wider than tall)
    angle_v = (wp.randf(rng) * 2.0 - 1.0) * fan_angle * 0.5

    # Direction toward wall (-Z) with fan spread
    dx = wp.sin(angle_h)
    dy = wp.sin(angle_v)
    dz = -wp.cos(angle_h) * wp.cos(angle_v)

    origins[i] = nozzle_pos
    directions[i] = wp.normalize(wp.vec3(dx, dy, dz))


@wp.kernel
def find_hits(
    origins: wp.array(dtype=wp.vec3),
    directions: wp.array(dtype=wp.vec3),
    wall_z: float,
    half_w: float,
    wall_h: float,
    max_range: float,
    hit_uvs: wp.array(dtype=wp.vec2),
    hit_flags: wp.array(dtype=int),
):
    """Check if ray hits the wall. Output UV of hit point."""
    i = wp.tid()
    hit_flags[i] = 0

    o = origins[i]
    d = directions[i]

    if wp.abs(d[2]) < 0.00000001:
        return

    t = (wall_z - o[2]) / d[2]

    if t < 0.0 or t > max_range:
        return

    hit_x = o[0] + t * d[0]
    hit_y = o[1] + t * d[1]

    if hit_x < -half_w or hit_x > half_w:
        return
    if hit_y < 0.0 or hit_y > wall_h:
        return

    u = (hit_x + half_w) / (2.0 * half_w)
    v = hit_y / wall_h

    hit_uvs[i] = wp.vec2(u, v)
    hit_flags[i] = 1


def spray_step(nozzle_x, nozzle_y, step_num):
    """Fire one burst of spray. Returns UV coordinates of hits."""
    n = config.SPRAY_DENSITY
    device = "cpu"

    origins = wp.zeros(n, dtype=wp.vec3, device=device)
    directions = wp.zeros(n, dtype=wp.vec3, device=device)
    hit_uvs = wp.zeros(n, dtype=wp.vec2, device=device)
    hit_flags = wp.zeros(n, dtype=int, device=device)

    nozzle = wp.vec3(nozzle_x, nozzle_y, config.NOZZLE_DISTANCE)

    wp.launch(shoot_spray, dim=n,
              inputs=[nozzle, config.FAN_ANGLE, step_num * n],
              outputs=[origins, directions], device=device)

    wp.launch(find_hits, dim=n,
              inputs=[origins, directions, 0.0,
                      config.WALL_WIDTH / 2.0, config.WALL_HEIGHT,
                      config.SPRAY_RANGE],
              outputs=[hit_uvs, hit_flags], device=device)

    wp.synchronize()

    uvs = hit_uvs.numpy()
    flags = hit_flags.numpy().astype(bool)
    return uvs[flags]
