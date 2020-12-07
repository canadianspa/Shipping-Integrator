from carriers.xdp.carrier import build_xdp_quotes
from carriers.dx.carrier import build_dx_quotes


def quotes_shipment_strategy(carrier):
    if "xdp" in carrier:
        return build_xdp_quotes(carrier)
    if carrier == "dx":
        return build_dx_quotes(carrier)
    else:
        raise ValueError(carrier)
