from carriers.xdp.carrier import delete_xdp_shipment


def delete_shipment_strategy(carrier, tracking_number):
    if "xdp" in carrier:
        return delete_xdp_shipment(carrier, tracking_number)
    else:
        raise ValueError(carrier)
