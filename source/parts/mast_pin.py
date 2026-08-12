from nurb import *


@part
def mast_pin(pin_width=5.1, pin_length=34.0, draft=False):
    """Alignment pin joining two stacked mast segments.

    pin_width: diameter of the pin
    pin_length: total pin length shared by the two mast segments
    """
    body = Cylinder(
        pin_width / 2,
        pin_length,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    if draft:
        return body
    # Keep the full-width bottom on the print bed. The polished top becomes the
    # tapered end that enters the mast socket with the conical roof.
    keep = body.edges().filter_by(lambda edge: edge.bounding_box().min.Z > 0)
    return polish(body, keep, 1.0)
