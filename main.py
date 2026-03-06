# main.py - Spray Paint Simulation
# Brings together all modules:
#   config.py      -> settings
#   wall.py        -> Task 1: cuboid wall mesh
#   spray.py       -> Task 2: Warp spray simulation
#   paint.py       -> Task 3: paint accumulation
#   nozzle_path.py -> Task 5: nozzle animation
#   main.py        -> Task 4: visualization + run simulation

from pxr import Usd, UsdGeom, UsdLux, Gf, Vt, Sdf
import numpy as np

import config
from wall import create_cuboid_wall
from spray import spray_step
from paint import PaintGrid
from nozzle_path import build_path


def save_static_usd(filename, paint_grid):
    """Save a single USD file showing the wall at current paint state."""
    stage = Usd.Stage.CreateNew(filename)
    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)

    # Build wall
    front, color_attr = create_cuboid_wall(stage)

    # Apply paint colors
    colors = paint_grid.get_face_colors()
    color_attr.Set(Vt.Vec3fArray(colors))

    # Add light
    light = UsdLux.DistantLight.Define(stage, "/World/DistantLight")
    light.CreateIntensityAttr().Set(1.0)

    stage.GetRootLayer().Save()


def run():
    path = build_path()
    total_steps = len(path)

    print("=" * 50)
    print("  Spray Paint Simulation")
    print("=" * 50)
    print(f"  Wall: {config.WALL_WIDTH}m x {config.WALL_HEIGHT}m x {config.WALL_DEPTH}m")
    print(f"  Spray density: {config.SPRAY_DENSITY} rays/step")
    print(f"  Fan angle: {config.FAN_ANGLE} rad")
    print(f"  Total steps: {total_steps}")
    print("=" * 50)

    # Initialize paint tracker
    paint = PaintGrid()

    # Save initial state (empty wall)
    save_static_usd("output/wall_initial.usda", paint)
    print("\nSaved: output/wall_initial.usda (empty wall)")

    # Create animated USD file
    anim_path = "output/spray_animation.usda"
    anim_stage = Usd.Stage.CreateNew(anim_path)
    UsdGeom.SetStageUpAxis(anim_stage, UsdGeom.Tokens.y)
    anim_stage.SetStartTimeCode(0)
    anim_stage.SetEndTimeCode(total_steps - 1)
    anim_stage.SetFramesPerSecond(24)

    # Build wall in animation file
    anim_front, anim_color = create_cuboid_wall(anim_stage)

    # Nozzle indicator (dark sphere)
    nozzle_xform = UsdGeom.Xform.Define(anim_stage, "/World/Nozzle")
    nozzle_shape = UsdGeom.Sphere.Define(anim_stage, "/World/Nozzle/Shape")
    nozzle_shape.GetRadiusAttr().Set(0.06)
    nozzle_shape.GetDisplayColorAttr().Set(
        Vt.Vec3fArray([Gf.Vec3f(0.15, 0.15, 0.15)]))

    # Light
    light = UsdLux.DistantLight.Define(anim_stage, "/World/DistantLight")
    light.CreateIntensityAttr().Set(1.0)

    # --- Run simulation ---
    print(f"\nSpraying {total_steps} steps...\n")

    for step in range(total_steps):
        nx, ny = path[step]

        # Task 2: Spray
        hits = spray_step(nx, ny, step)

        # Task 3: Accumulate paint
        paint.add_paint(hits)

        # Task 4: Update animation frame
        colors = paint.get_face_colors()
        anim_color.Set(Vt.Vec3fArray(colors), time=step)

        # Task 5: Move nozzle
        nozzle_xform.ClearXformOpOrder()
        op = nozzle_xform.AddTranslateOp()
        op.Set(Gf.Vec3d(nx, ny, config.NOZZLE_DISTANCE), time=step)

        # Progress
        if (step + 1) % 40 == 0:
            cov = paint.get_coverage()
            print(f"  Step {step+1}/{total_steps}: "
                  f"nozzle=({nx:+.2f}, {ny:.2f}) "
                  f"coverage={cov:.1f}%")

        # Save midway snapshot
        if step + 1 == total_steps // 2:
            save_static_usd("output/wall_midway.usda", paint)
            print(f"  >> Saved: output/wall_midway.usda")

    # Save animation
    anim_stage.GetRootLayer().Save()

    # Save final snapshot
    save_static_usd("output/wall_final.usda", paint)

    print(f"\n{'=' * 50}")
    print(f"  Done! Coverage: {paint.get_coverage():.1f}%")
    print(f"{'=' * 50}")
    print(f"\n  Screenshots (press 4 to remove wireframe):")
    print(f"    usdview output/wall_initial.usda")
    print(f"    usdview output/wall_midway.usda")
    print(f"    usdview output/wall_final.usda")
    print(f"\n  Animation:")
    print(f"    usdview output/spray_animation.usda")
    print(f"    Press 4, then Play!")


if __name__ == "__main__":
    run()
