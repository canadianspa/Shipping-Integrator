from carriers.xdp.quotes_xdp import build_xdp_quotes


def quotes_shipment_strategy(carrier):
    if "xdp" in carrier:
        return build_xdp_quotes()
    else:
        raise ValueError(carrier)
