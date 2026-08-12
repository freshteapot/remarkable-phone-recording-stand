from nurb import *


def B(x, y, z):
    return Box(x, y, z, align=(Align.MIN, Align.MIN, Align.MIN))


@part
def iphone_12_mini_cradle(phone_case_width=70.0,
                          phone_case_height=136.0,
                          phone_case_thickness=11.0, fit=0.6,
                          rail_width=8.0, support_lip=10.0,
                          camera_adjustment=60.0, draft=False):
    """Fitted everyday cradle for the cased iPhone 12 mini.

    phone_case_width: measured width of the cased phone
    phone_case_height: full height of the cased phone
    phone_case_thickness: thickness of the phone and case together
    fit: extra width for inserting and removing the phone
    rail_width: width of the side frame rails
    support_lip: length of the lower phone support
    camera_adjustment: sideways travel at the standard tower mount
    """
    inside = phone_case_width + fit
    length = phone_case_height + 4.0
    wall_height = phone_case_thickness + 2.0
    left = B(rail_width, length, wall_height).translate((-inside / 2 - rail_width, -length / 2, 0))
    right = B(rail_width, length, wall_height).translate((inside / 2, -length / 2, 0))
    bottom = B(inside, support_lip, 5.0).translate((-inside / 2, -length / 2, 0))
    upper_right = B(support_lip, support_lip, 5.0).translate((inside / 2 - support_lip, length / 2 - support_lip, 0))
    body = left + right + bottom + upper_right

    # One elastic retainer prevents the fitted phone lifting without obscuring its cameras.
    for x in (-inside / 2 - rail_width - 1, inside / 2 - 1):
        body -= B(rail_width + 2, 8.0, 5.0).translate((x, -4.0, 5.0))

    mount = B(camera_adjustment + 16, 44, 5.0).translate((-camera_adjustment / 2 - 8, length / 2 - 32, 0))
    body += mount
    for y in (length / 2 - 24, length / 2 - 14, length / 2 - 4):
        body -= B(camera_adjustment, 6.4, 5.0).translate((-camera_adjustment / 2, y - 3.2, 0))
    if draft:
        return body
    concave = concave_edges(body)
    keep = body.edges().filter_by(lambda e: e.bounding_box().min.Z > 0 and e not in concave)
    return polish(body, keep, 1.0)
