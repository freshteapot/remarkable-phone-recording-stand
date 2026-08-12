from nurb import *


@part
def cradle_lock_pin(pin_width=5.8, joined_thickness=21.0,
                    head_width=16.0, head_thickness=3.0,
                    clip_neck_width=4.4, clip_groove_width=2.4,
                    axial_clearance=0.3, draft=False):
    """Headed tool-free pin joining a phone cradle to the boom.

    pin_width: diameter passing through the existing cradle and boom slots
    joined_thickness: combined thickness of the cradle mount and boom
    head_width: finger-grip diameter at the top of the pin
    head_thickness: thickness of the finger-grip head
    clip_neck_width: diameter of the groove where the retaining clip snaps
    clip_groove_width: height of the retaining-clip groove
    axial_clearance: free movement between the joined parts and retaining clip
    """
    if pin_width >= 6.4:
        reject("pin_width must stay below the existing 6.4mm mount opening", param="pin_width")
    head = Cylinder(head_width / 2, head_thickness, align=(Align.CENTER, Align.CENTER, Align.MIN))
    shoulder_length = joined_thickness + axial_clearance
    shoulder = Cylinder(pin_width / 2, shoulder_length, align=(Align.CENTER, Align.CENTER, Align.MIN)).translate((0, 0, head_thickness))
    neck = Cylinder(clip_neck_width / 2, clip_groove_width, align=(Align.CENTER, Align.CENTER, Align.MIN)).translate((0, 0, head_thickness + shoulder_length))
    tip_z = head_thickness + shoulder_length + clip_groove_width
    flare_height = (pin_width - clip_neck_width) / 2
    flare = Cone(clip_neck_width / 2, pin_width / 2, flare_height, align=(Align.CENTER, Align.CENTER, Align.MIN)).translate((0, 0, tip_z))
    tip = Cylinder(pin_width / 2, 2.6 - flare_height, align=(Align.CENTER, Align.CENTER, Align.MIN)).translate((0, 0, tip_z + flare_height))
    body = head + shoulder + neck + flare + tip
    if draft:
        return body
    concave = concave_edges(body)
    keep = body.edges().filter_by(lambda e: e.bounding_box().min.Z > 0 and e not in concave)
    return polish(body, keep, 1.0)
