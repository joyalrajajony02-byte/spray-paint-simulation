# wall.py - A vertical cuboid wall
# This is a 3D box: front face, back face, top, bottom, left, right
# The front face is subdivided into a grid so we can paint it

from pxr import Usd, UsdGeom, Gf, Vt, Sdf
import config

def create_cuboid_wall(stage):
    """
    Create a wall that looks like a real wall:
    - Front face: subdivided grid (this is where paint goes)
    - Back, top, bottom, left, right: simple gray faces
    """
    n = config.GRID_RES
    w = config.WALL_WIDTH
    h = config.WALL_HEIGHT
    d = config.WALL_DEPTH
    hw = w / 2.0   # half width

    # ========== FRONT FACE (paintable, subdivided) ==========
    front = UsdGeom.Mesh.Define(stage, "/World/Wall/Front")

    # Grid of points on the front face (Z = 0)
    points = []
    for row in range(n + 1):
        for col in range(n + 1):
            x = -hw + (col / n) * w
            y = (row / n) * h
            points.append(Gf.Vec3f(x, y, 0.0))

    # Connect into square faces
    face_sizes = []
    face_indices = []
    for row in range(n):
        for col in range(n):
            bl = row * (n + 1) + col       # bottom-left
            br = bl + 1                     # bottom-right
            tr = br + (n + 1)              # top-right
            tl = bl + (n + 1)              # top-left
            face_sizes.append(4)
            face_indices.extend([bl, br, tr, tl])

    front.GetPointsAttr().Set(Vt.Vec3fArray(points))
    front.GetFaceVertexCountsAttr().Set(Vt.IntArray(face_sizes))
    front.GetFaceVertexIndicesAttr().Set(Vt.IntArray(face_indices))

    # Color attribute for painting
    color_attr = UsdGeom.PrimvarsAPI(front).CreatePrimvar(
        "displayColor", Sdf.ValueTypeNames.Color3fArray, UsdGeom.Tokens.uniform
    )

    # ========== OTHER 5 FACES (simple gray boxes) ==========
    sides = UsdGeom.Mesh.Define(stage, "/World/Wall/Sides")

    # 8 corners of the cuboid
    side_points = Vt.Vec3fArray([
        Gf.Vec3f(-hw, 0, 0),       # 0: front bottom-left
        Gf.Vec3f( hw, 0, 0),       # 1: front bottom-right
        Gf.Vec3f( hw, h, 0),       # 2: front top-right
        Gf.Vec3f(-hw, h, 0),       # 3: front top-left
        Gf.Vec3f(-hw, 0, -d),      # 4: back bottom-left
        Gf.Vec3f( hw, 0, -d),      # 5: back bottom-right
        Gf.Vec3f( hw, h, -d),      # 6: back top-right
        Gf.Vec3f(-hw, h, -d),      # 7: back top-left
    ])

    # 5 faces: back, left, right, top, bottom (skip front)
    side_counts = Vt.IntArray([4, 4, 4, 4, 4])
    side_indices = Vt.IntArray([
        5, 4, 7, 6,    # back
        4, 0, 3, 7,    # left
        1, 5, 6, 2,    # right
        3, 2, 6, 7,    # top
        4, 5, 1, 0,    # bottom
    ])

    sides.GetPointsAttr().Set(side_points)
    sides.GetFaceVertexCountsAttr().Set(side_counts)
    sides.GetFaceVertexIndicesAttr().Set(side_indices)
    sides.GetDisplayColorAttr().Set(Vt.Vec3fArray([Gf.Vec3f(0.75, 0.75, 0.72)]))

    return front, color_attr
