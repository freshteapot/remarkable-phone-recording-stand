from nurb import *


def B(x, y, z):
    return Box(x, y, z, align=(Align.MIN, Align.MIN, Align.MIN))


@part
def recording_mast(mast_height=220.0, mast_width=24.0, mast_depth=18.0,
                   pin_width=5.4, pin_spacing=11.0, pin_socket_depth=18.0,
                   draft=False):
    """Stackable tower segment; print four for the full stand.

    mast_height: height added by one tower segment
    mast_width: side-to-side size of the structural column
    mast_depth: front-to-back size of the structural column
    pin_width: diameter of the two alignment-pin holes
    pin_spacing: distance between the alignment-pin centers
    pin_socket_depth: depth of each stopped alignment-pin socket
    """
    body = B(mast_width, mast_depth, mast_height).translate((-mast_width / 2, -mast_depth / 2, 0))
    cone_height = pin_width / 2
    for x in (-pin_spacing / 2, pin_spacing / 2):
        # The bottom socket closes with a 45-degree conical roof, so it prints
        # support-free instead of bridging a circular ceiling.
        bottom_socket = Cylinder(
            pin_width / 2,
            pin_socket_depth - cone_height,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).translate((x, 0, 0))
        bottom_socket += Cone(
            pin_width / 2,
            0,
            cone_height,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).translate((x, 0, pin_socket_depth - cone_height))
        top_socket = Cylinder(
            pin_width / 2,
            pin_socket_depth,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        ).translate((x, 0, mast_height - pin_socket_depth))
        body -= bottom_socket + top_socket
    if draft:
        return body
    concave = concave_edges(body)
    keep = body.edges().filter_by(lambda e: e.bounding_box().min.Z > body.bounding_box().min.Z and e not in concave)
    return polish(body, keep, 1.0)
