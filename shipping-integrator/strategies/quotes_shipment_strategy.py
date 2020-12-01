from carriers.xdp.carrier import build_xdp_quotes


def quotes_shipment_strategy(carrier):
    if "xdp" in carrier:
        return build_xdp_quotes()
    else:
        raise ValueError(carrier)
