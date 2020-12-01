from carriers.xdp.carrier import create_xdp_shipment


def create_shipment_strategy(carrier, shipment):
    if "xdp" in carrier:
        return create_xdp_shipment(carrier, shipment)
    else:
        raise ValueError(carrier)
