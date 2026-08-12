from nurb import *


def B(x, y, z):
    return Box(x, y, z, align=(Align.MIN, Align.MIN, Align.MIN))


@part
def recording_base(base_width=190.0, base_depth=230.0, rail_width=28.0,
                   base_thickness=8.0, tower_spacing=130.0,
                   mast_socket_width=24.2, mast_socket_depth=18.2,
                   alignment_pin_width=5.2, alignment_pin_spacing=11.0,
                   alignment_pin_engagement=12.0,
                   draft=False):
    """Open footprint that counterbalances the overhead phone.

    base_width: side-to-side width behind the tablet
    base_depth: distance the feet extend behind the tablet
    rail_width: width of each foot and joining rail
    base_thickness: thickness of the frame on the desk
    tower_spacing: distance between the two tower columns
    mast_socket_width: side-to-side opening around each mast
    mast_socket_depth: front-to-back opening around each mast
    alignment_pin_width: diameter of the two dowels inside each socket
    alignment_pin_spacing: distance between the dowel centers
    alignment_pin_engagement: depth each dowel enters the mast bottom
    """
    left = B(rail_width, base_depth, base_thickness).translate((-base_width / 2, -base_depth, 0))
    right = B(rail_width, base_depth, base_thickness).translate((base_width / 2 - rail_width, -base_depth, 0))
    rear = B(base_width, rail_width, base_thickness).translate((-base_width / 2, -base_depth, 0))
    front = B(base_width, rail_width, base_thickness).translate((-base_width / 2, -rail_width, 0))
    body = left + right + rear + front
    for x in (-tower_spacing / 2, tower_spacing / 2):
        boss = B(30, 28, 18).translate((x - 15, -28, 0))
        socket = B(mast_socket_width, mast_socket_depth, 14).translate(
            (x - mast_socket_width / 2, -14 - mast_socket_depth / 2, 6)
        )
        body = (body + boss) - socket
        for pin_x in (-alignment_pin_spacing / 2, alignment_pin_spacing / 2):
            pin = Cylinder(
                alignment_pin_width / 2,
                alignment_pin_engagement,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).translate((x + pin_x, -14.0, 6.0))
            body += pin
    if draft:
        return body
    bed = body.bounding_box().min.Z
    concave = concave_edges(body)
    keep = body.edges().filter_by(lambda e: e.bounding_box().min.Z > bed and e not in concave)
    return polish(body, keep, 1.0)
