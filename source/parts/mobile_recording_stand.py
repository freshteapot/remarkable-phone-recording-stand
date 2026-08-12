from nurb import *


@assembly
def mobile_recording_stand(tower_height=446.0, phone_height=466.0):
    """Preview of the complete handed-neutral recording stand.

    tower_height: height of the stacked column pair
    phone_height: height of the phone cradle over the desk
    """
    base = use("recording_base")
    masts = [
        use("recording_mast").translate((-65, -14, 6)),
        use("recording_mast").translate((65, -14, 6)),
        use("recording_mast").translate((-65, -14, 226)),
        use("recording_mast").translate((65, -14, 226)),
    ]
    joining_collars = [
        use("mast_cam_collar").translate((-65, -14, 204)),
        use("mast_cam_collar").translate((65, -14, 204)),
    ]
    boom = use("recording_boom").rotate(Axis.Y, 180).translate(
        (0, -14, tower_height + 20)
    )
    cradle = use("iphone_12_mini_cradle").translate((0, 97, phone_height))
    lock_pin = use("cradle_lock_pin").rotate(Axis.X, 180).translate((0, 163, phone_height + 8))
    retaining_clip = use("cradle_retaining_clip").translate(
        (0, 163, phone_height - 18.0)
    )
    tablet = obstacle(Box(measured("remarkable_width"), measured("remarkable_height"), measured("remarkable_thickness"), align=(Align.MIN, Align.MIN, Align.MIN)).translate((-94, 20, 0)), "reMarkable 2 envelope")
    return [
        base,
        *masts,
        *joining_collars,
        boom,
        cradle,
        lock_pin,
        retaining_clip,
        tablet,
    ]
