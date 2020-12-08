from carriers.xdp.carrier import create_xdp_shipment
from carriers.dx.carrier import create_dx_shipment


def create_shipment_strategy(carrier, shipment):
    if "xdp" in carrier:
        return create_xdp_shipment(carrier, shipment)
    elif carrier == "dx":
        return create_dx_shipment(shipment)
    else:
        raise ValueError(carrier)
