from nurb import *


def B(x, y, z):
    return Box(x, y, z, align=(Align.MIN, Align.MIN, Align.MIN))


@part
def cradle_retaining_clip(outer_width=14.0, neck_fit_width=4.7,
                          snap_gap=4.2, clip_thickness=2.0,
                          thumb_tab_length=7.0, draft=False):
    """Side-snapping C-clip for the tool-free cradle locking pin.

    outer_width: outside diameter of the retaining ring
    neck_fit_width: inside diameter around the pin groove
    snap_gap: narrow entrance that flexes over the pin neck
    clip_thickness: printed thickness of the clip
    thumb_tab_length: length of the removal tab opposite the opening
    """
    if snap_gap >= neck_fit_width:
        reject("snap_gap must be narrower than neck_fit_width so the clip retains", param="snap_gap")
    outer = Cylinder(outer_width / 2, clip_thickness, align=(Align.CENTER, Align.CENTER, Align.MIN))
    inner = Cylinder(neck_fit_width / 2, clip_thickness, align=(Align.CENTER, Align.CENTER, Align.MIN))
    opening = B(outer_width / 2 + 1, snap_gap, clip_thickness).translate((0, -snap_gap / 2, 0))
    ring = (outer - inner) - opening
    tab = B(thumb_tab_length, 8.0, clip_thickness).translate((-outer_width / 2 - thumb_tab_length + 3, -4.0, 0))
    body = ring + tab
    if draft:
        return body
    concave = concave_edges(body)
    keep = body.edges().filter_by(lambda e: e.bounding_box().min.Z > 0 and e not in concave)
    return polish(body, keep, 1.0)
