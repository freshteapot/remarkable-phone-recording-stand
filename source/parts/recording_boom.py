from nurb import *


def B(x, y, z):
    return Box(x, y, z, align=(Align.MIN, Align.MIN, Align.MIN))


@part
def recording_boom(tower_spacing=130.0, reach=177.0, beam_width=24.0,
                   beam_thickness=16.0, mast_socket_width=24.2,
                   mast_socket_depth=18.2, mast_engagement=14.0,
                   alignment_pin_width=5.2, alignment_pin_spacing=11.0,
                   alignment_pin_engagement=12.0,
                   draft=False):
    """Flat-printing twin-arm boom for a centered overhead phone.

    tower_spacing: distance between tower columns
    reach: distance from tower to phone mount
    beam_width: width of each structural rail
    beam_thickness: printed thickness of the boom
    mast_socket_width: side-to-side opening around each mast
    mast_socket_depth: front-to-back opening around each mast
    mast_engagement: depth each mast enters its stopped boom socket
    alignment_pin_width: diameter of the two dowels inside each mast collar
    alignment_pin_spacing: distance between the dowel centers
    alignment_pin_engagement: depth each dowel enters the mast end socket
    """
    # The rear bridge is wide enough to ground the 30mm stopped socket collars.
    overall_width = tower_spacing + 30.0
    # The mast/socket centerline is local y=0. Keeping `reach` measured from
    # that datum prevents the entire boom from sitting half a beam forward of
    # the tower in the assembly.
    rear_y = -beam_width / 2
    rear = B(overall_width, beam_width, beam_thickness).translate((-overall_width / 2, rear_y, 0))
    arm_length = reach + beam_width / 2
    left = B(beam_width, arm_length, beam_thickness).translate((-tower_spacing / 2 - beam_width / 2, rear_y, 0))
    right = B(beam_width, arm_length, beam_thickness).translate((tower_spacing / 2 - beam_width / 2, rear_y, 0))
    front = B(overall_width, beam_width, beam_thickness).translate((-overall_width / 2, reach - beam_width, 0))
    pad = B(50, 42, beam_thickness).translate((-25, reach - 21, 0))
    body = rear + left + right + front + pad
    for x in (-tower_spacing / 2, tower_spacing / 2):
        # These collars print upward on the rear beam. In use the boom flips over,
        # placing the openings downward while the solid beam becomes the mast stop.
        collar = B(30.0, beam_width, mast_engagement + 4.0).translate(
            (x - 15.0, rear_y, beam_thickness)
        )
        socket = B(mast_socket_width, mast_socket_depth, mast_engagement).translate(
            (
                x - mast_socket_width / 2,
                -mast_socket_depth / 2,
                beam_thickness + 4.0,
            )
        )
        body = (body + collar) - socket
        for pin_x in (-alignment_pin_spacing / 2, alignment_pin_spacing / 2):
            pin = Cylinder(
                alignment_pin_width / 2,
                alignment_pin_engagement,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            ).translate((x + pin_x, 0, beam_thickness + 4.0))
            body += pin
    body -= Cylinder(3.2, beam_thickness, align=(Align.CENTER, Align.CENTER, Align.MIN)).translate((0, reach, 0))
    if draft:
        return body
    concave = concave_edges(body)
    keep = body.edges().filter_by(lambda e: e.bounding_box().min.Z > body.bounding_box().min.Z and e not in concave)
    return polish(body, keep, 1.0)
