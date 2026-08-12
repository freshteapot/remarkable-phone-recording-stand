from nurb import *


def B(x, y, z):
    return Box(x, y, z, align=(Align.MIN, Align.MIN, Align.MIN))


@part
def phone_cradle(max_phone_width=84.0, max_phone_height=174.0,
                 max_phone_thickness=14.0, rail_width=10.0,
                 support_lip=14.0, frame_thickness=5.0,
                 camera_adjustment=60.0, draft=False):
    """Elastic-retained universal frame with an open camera area.

    max_phone_width: widest cased phone the frame accepts
    max_phone_height: tallest cased phone the frame accepts
    max_phone_thickness: thickest cased phone the side walls accept
    rail_width: width of the outside frame rails
    support_lip: inward reach supporting compact phones
    frame_thickness: material below the phone
    camera_adjustment: sideways travel for centering different camera layouts
    """
    width = max_phone_width
    length = max_phone_height
    wall_height = max_phone_thickness + 2.0

    left = B(rail_width, length, wall_height).translate((-width / 2 - rail_width, -length / 2, 0))
    right = B(rail_width, length, wall_height).translate((width / 2, -length / 2, 0))
    bottom = B(width, support_lip, frame_thickness).translate((-width / 2, -length / 2, 0))
    upper_right = B(support_lip, support_lip, frame_thickness).translate((width / 2 - support_lip, length / 2 - support_lip, 0))
    body = left + right + bottom + upper_right

    # Four pass-throughs take two ordinary elastic bands over the phone's screen.
    for y in (-length * 0.20, length * 0.20):
        body -= B(rail_width + 2, 8.0, 5.0).translate((-width / 2 - rail_width - 1, y - 4, 5))
        body -= B(rail_width + 2, 8.0, 5.0).translate((width / 2 - 1, y - 4, 5))

    mount = B(camera_adjustment + 16, 44, frame_thickness).translate((-camera_adjustment / 2 - 8, length / 2 - 32, 0))
    body += mount
    for y in (length / 2 - 24, length / 2 - 14, length / 2 - 4):
        body -= B(camera_adjustment, 6.4, frame_thickness).translate((-camera_adjustment / 2, y - 3.2, 0))
    if draft:
        return body
    concave = concave_edges(body)
    keep = body.edges().filter_by(lambda e: e.bounding_box().min.Z > body.bounding_box().min.Z and e not in concave)
    return polish(body, keep, 1.0)
