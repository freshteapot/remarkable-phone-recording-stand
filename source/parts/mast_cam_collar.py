from nurb import *


def B(x, y, z):
    return Box(x, y, z, align=(Align.MIN, Align.MIN, Align.MIN))


@part
def mast_cam_collar(mast_opening_width=24.2,
                    mast_opening_depth=18.2,
                    collar_height=44.0,
                    collar_wall=2.0,
                    cam_pressure=0.15,
                    moving_clearance=0.35,
                    draft=False):
    """Print-in-place quarter-turn cam collar for a mast joint.

    mast_opening_width: side-to-side opening that slides over the mast
    mast_opening_depth: front-to-back opening that slides over the mast
    collar_height: total sleeve height shared above and below the joint
    collar_wall: thickness surrounding the smooth mast opening
    cam_pressure: inward squeeze when the cam is turned to lock
    moving_clearance: print gap around the rotating cam
    """
    cam_radius = 2.7
    flat_depth = 0.5
    bearing_radius = cam_radius + moving_clearance
    outer_width = mast_opening_width + 2 * collar_wall
    outer_depth = mast_opening_depth + 2 * collar_wall
    inner_front = mast_opening_depth / 2
    axis_y = inner_front + cam_radius - cam_pressure

    sleeve = B(outer_width, outer_depth, collar_height).translate(
        (-outer_width / 2, -outer_depth / 2, 0)
    )
    boss = B(14.0, 8.0, collar_height).translate(
        (-7.0, outer_depth / 2 - 2.0, 0)
    )
    body = sleeve + boss
    if not draft:
        bed = body.bounding_box().min.Z
        exposed = body.edges().filter_by(
            lambda edge: edge.bounding_box().min.Z > bed
        )
        body = polish(body, exposed, 1.0)

    mast_opening = B(
        mast_opening_width,
        mast_opening_depth,
        collar_height + 2.0,
    ).translate(
        (-mast_opening_width / 2, -mast_opening_depth / 2, -1.0)
    )
    bearing = Cylinder(
        bearing_radius,
        collar_height + 2.0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).translate((0, axis_y, -1.0))
    body -= mast_opening + bearing

    # The cam prints with its flat facing the mast. That gives 0.35 mm sliding
    # clearance. A quarter-turn presents the round face and adds 0.15 mm grip.
    cam = Cylinder(
        cam_radius,
        collar_height,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).translate((0, axis_y, 0))
    flat_y = axis_y - cam_radius + flat_depth
    flat_cut = B(8.0, 4.0, collar_height + 2.0).translate(
        (-4.0, flat_y - 4.0, -1.0)
    )
    cam -= flat_cut

    # The upright finger tab shows the flat's direction and turns the cam.
    finger_tab = B(5.0, 1.4, 8.0).translate(
        (-2.5, axis_y - 0.2, collar_height)
    )
    cam += finger_tab

    # Two bead-sized bridges make the exported prototype one object. The first
    # deliberate twist snaps them, after which the cam rotates in its bearing.
    bridges = None
    for side in (-1, 1):
        bridge = B(0.6, 0.5, 0.7).translate(
            (
                side * (cam_radius + moving_clearance / 2) - 0.3,
                axis_y - 0.25,
                collar_height - 0.1,
            )
        )
        bridges = bridge if bridges is None else bridges + bridge

    return body + cam + bridges
