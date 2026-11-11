"""Snap-fit case for the zigbee-c6-dongle. Run: python3 case.py  (needs cadquery)

Frame: X along the board from the USB end, Y across it, Z up.
The board's bottom face is Z=0 and its USB-end corner on the indexing-hole
side is the origin. All dimensions in mm.
"""
import cadquery as cq

# ---- board -----------------------------------------------------------------
BL, BW, BT = 58.25, 20.75, 1.6          # board length, width, thickness
H1, H2 = (11.65, 2.0), (56.0, 2.0)      # 2.0 mm indexing holes
SW_RST, SW_BOOT = (22.75, 16.35), (16.68, 5.475)
LED_STATUS, LED_PWR = (4.0, 19.25), (3.25, 1.95)
JST = [(31.225, "I2C"), (40.5, "UART")]  # connector centres along X (on the Y=BW edge)
PLUG_Y = (4.72, 16.73)                  # USB-A shell extent across the board
HOLD = [(6.6, 14.6), (18.5, 11.0), (36.2, 11.1), (53.4, 1.3)]  # free spots on the top side

# ---- case ------------------------------------------------------------------
C = 0.3            # clearance board edge to wall
WALL = 1.6         # side walls
WALL_USB = 2.0     # end wall at the USB plug
WALL_SMA = 2.0     # end wall carrying the SMA bulkhead
FLOOR = 1.2
LID = 1.6
CAV = 14.0         # antenna pigtail bay behind the board
Z_FLOOR = -5.0     # inner floor (USB plug body hangs 4.5 below the board)
Z_TOP = 6.0        # top of base walls / underside of lid
SMA_D = 6.6        # 1/4"-36 bulkhead thread with clearance
SMA_Z = 0.5
PEG_D = 1.7
FIT = 0.25         # gap between mating printed faces

X0, X1 = -C - WALL_USB, BL + C + CAV + WALL_SMA
Y0, Y1 = -C - WALL, BW + C + WALL
XI0, XI1 = -C, BL + C + CAV
YI0, YI1 = -C, BW + C
YC = BW / 2

HOOK_X, HOOK_W, HOOK_T = BL + C + 7.0, 8.0, 1.2
HOOK_GAP, HOOK_CATCH = 0.2, 0.6
HOOK_ZTIP = -1.6
TONGUES = [(0.6, 3.4), (BW - 3.4, BW - 0.6)]
TONGUE_Z = (3.45, 4.75)


def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))


def outer(z0, z1):
    return box(X0, X1, Y0, Y1, z0, z1).edges("|Z").fillet(2.0)


def make_base():
    b = outer(Z_FLOOR - FLOOR, Z_TOP)
    b = b.faces("<Z").chamfer(0.4)
    b = b.cut(box(XI0, XI1, YI0, YI1, Z_FLOOR, Z_TOP + 1).edges("|Z").fillet(0.5))
    # board rests on two ledges and two peg posts
    for y0, y1 in ((YI0, 0.8), (BW - 0.8, YI1)):
        b = b.union(box(XI0, BL + C, y0, y1, Z_FLOOR, 0))
    for (x, y) in (H1, H2):
        post = cq.Workplane("XY").circle(2.25).extrude(-Z_FLOOR).translate((x, y, Z_FLOOR))
        peg = cq.Workplane("XY").circle(PEG_D / 2).extrude(BT + 1.0).faces(">Z").chamfer(0.3).translate((x, y, 0))
        b = b.union(post).union(peg)
    # USB plug notch, open to the top so the board drops straight in
    b = b.cut(box(X0 - 1, XI0 + 0.01, PLUG_Y[0] - 0.32, PLUG_Y[1] + 0.32, Z_FLOOR + 0.1, Z_TOP + 1))
    # slots for the lid's toe-in tongues
    for y0, y1 in TONGUES:
        b = b.cut(box(XI0 - 1.3, XI0 + 0.01, y0 - FIT, y1 + FIT, TONGUE_Z[0] - FIT, TONGUE_Z[1] + FIT))
    # JST-SH (Qwiic) windows
    for x, _ in JST:
        b = b.cut(box(x - 3.7, x + 3.7, YI1 - 0.01, Y1 + 1, BT - 0.2, BT + 3.4))
    # SMA bulkhead hole
    b = b.cut(cq.Workplane("YZ").circle(SMA_D / 2).extrude(WALL_SMA + 2).translate((XI1 - 1, YC, SMA_Z)))
    # windows the lid hooks latch into
    for ys in ((Y0 - 1, YI0 + 0.01), (YI1 - 0.01, Y1 + 1)):
        b = b.cut(box(HOOK_X - HOOK_W / 2 - 0.5, HOOK_X + HOOK_W / 2 + 0.5, ys[0], ys[1], HOOK_ZTIP - 0.6, 0.2))
    # lead-in chamfer for the hooks on the wall's inner top edge
    for y, s in ((YI0, -1), (YI1, 1)):
        tri = (cq.Workplane("YZ").polyline([(y - 0.01 * s, Z_TOP + 0.01), (y + 0.8 * s, Z_TOP + 0.01), (y - 0.01 * s, Z_TOP - 0.8)]).close()
               .extrude(HOOK_W + 1.0).translate((HOOK_X - HOOK_W / 2 - 0.5, 0, 0)))
        b = b.cut(tri)
    return b


def hook(side):
    """Cantilever hook hanging from the lid. side=-1 at Y=YI0, +1 at Y=YI1."""
    yw = YI0 if side < 0 else YI1          # inner wall face
    f = yw - side * HOOK_GAP               # hook face nearest the wall
    back = f - side * HOOK_T
    tip = f + side * HOOK_CATCH
    pts = [(back, Z_TOP), (f, Z_TOP), (f, 0.2), (tip, -0.2), (tip, -0.6), (f, HOOK_ZTIP), (back, HOOK_ZTIP)]
    h = cq.Workplane("YZ").polyline(pts).close().extrude(HOOK_W).translate((HOOK_X - HOOK_W / 2, 0, 0))
    # root gusset for strength across the layer lines
    g = (cq.Workplane("YZ").polyline([(back, Z_TOP), (back - side * 1.5, Z_TOP), (back, Z_TOP - 1.5)]).close()
         .extrude(HOOK_W).translate((HOOK_X - HOOK_W / 2, 0, 0)))
    return h.union(g)


def flexure(lid, cx, cy, label_y, label):
    """Thin spring tab with a plunger over a tact switch."""
    tab_w, slot = 5.0, 0.6
    x_free, x_root = cx - 2.75, cx + 8.75
    y0, y1 = cy - tab_w / 2, cy + tab_w / 2
    region = box(x_free - slot, x_root, y0 - slot, y1 + slot, Z_TOP - 0.01, Z_TOP + LID + 1)
    tab = box(x_free, x_root + 1, y0, y1, Z_TOP + LID - 0.8, Z_TOP + LID)
    lid = lid.cut(region).union(tab)
    plunger = cq.Workplane("XY").circle(1.6).extrude(Z_TOP + LID - 0.8 - (BT + 1.5 + 0.3)).translate((cx, cy, BT + 1.5 + 0.3))
    lid = lid.union(plunger)
    return lid


def make_lid():
    l = outer(Z_TOP, Z_TOP + LID)
    l = l.faces(">Z").chamfer(0.4)
    # tab closing the USB notch above the plug
    l = l.union(box(X0, XI0, PLUG_Y[0] - 0.32 + FIT, PLUG_Y[1] + 0.32 - FIT, 0.8, Z_TOP))
    # toe-in tongues at the USB end
    for y0, y1 in TONGUES:
        prof = [(XI0 + 0.2, Z_TOP), (XI0 + 0.2, TONGUE_Z[1]), (XI0 - 0.3, TONGUE_Z[1]), (XI0 - 1.05, TONGUE_Z[0] + 0.5),
                (XI0 - 1.05, TONGUE_Z[0]), (XI0 + 2.1, TONGUE_Z[0]), (XI0 + 2.1, Z_TOP)]
        t = cq.Workplane("XZ").polyline(prof).close().extrude(-(y1 - y0)).translate((0, y0, 0))
        l = l.union(t)
    # snap hooks in the antenna bay
    l = l.union(hook(-1)).union(hook(1))
    # hold-down posts
    for (x, y) in HOLD:
        l = l.union(cq.Workplane("XY").circle(0.9).extrude(Z_TOP - BT - 0.15).translate((x, y, BT + 0.15)))
    # buttons
    l = flexure(l, *SW_RST, None, "RST")
    l = flexure(l, *SW_BOOT, None, "BOOT")
    # LED windows
    for (x, y) in (LED_STATUS, LED_PWR):
        l = l.cut(cq.Workplane("XY").circle(0.8).extrude(LID + 2).translate((x, y, Z_TOP - 1)))
    # engraved labels
    top = Z_TOP + LID
    labels = [("RST", 23.0, Y1 - 1.75), ("BOOT", 21.0, Y0 + 1.75), ("I2C", JST[0][0] + 1.0, Y1 - 1.75), ("UART", JST[1][0] + 1.5, Y1 - 1.75)]
    for s, x, y in labels:
        txt = cq.Workplane("XY").workplane(offset=top).center(x, y).text(s, 2.4, -0.4, kind="bold", halign="center", valign="center")
        l = l.cut(txt)
    return l


if __name__ == "__main__":
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    base, lid = make_base(), make_lid()
    for name, part in (("base", base), ("lid", lid)):
        cq.exporters.export(part, os.path.join(here, f"dongle-case-{name}.step"))
    # STL in print orientation: base as modelled, lid flipped so its outer face is on the bed
    cq.exporters.export(base.translate((0, 0, -(Z_FLOOR - FLOOR))), os.path.join(here, "dongle-case-base.stl"), tolerance=0.02, angularTolerance=0.1)
    lid_print = lid.rotate((0, 0, 0), (1, 0, 0), 180).translate((0, 0, Z_TOP + LID))
    cq.exporters.export(lid_print, os.path.join(here, "dongle-case-lid.stl"), tolerance=0.02, angularTolerance=0.1)
    for name, part in (("base", base), ("lid", lid)):
        bb = part.val().BoundingBox()
        print(name, "solids", part.solids().size(), "size %.2f x %.2f x %.2f" % (bb.xlen, bb.ylen, bb.zlen), "volume %.0f mm3" % part.val().Volume())
