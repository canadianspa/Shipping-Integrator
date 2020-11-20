from carriers.xdp.quotes_xdp import build_xdp_quotes


def QuotesFactory(carrier):
    if "xdp" in carrier:
        return build_xdp_quotes()
    elif carrier == "dx_freight":
        return []
    else:
        raise ValueError(carrier)
