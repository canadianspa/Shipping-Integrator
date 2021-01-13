from carriers.xdp.carrier import redirect_xdp_tracking
from carriers.dx.carrier import redirect_dx_tracking


def track_shipment_strategy(carrier, tracking_number):
    if "xdp" in carrier:
        return redirect_xdp_tracking(tracking_number)
    elif carrier == "dx":
        return redirect_dx_tracking(tracking_number)
    else:
        raise ValueError(carrier)
