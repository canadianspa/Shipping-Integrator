from .service import Service


def ServiceFactory(carrier):
    if carrier == "xdp":
        return [
            Service("xdp", "XDP Test", "collection")
        ]
    elif carrier == "dx_freight":
        return []
    else:
        raise ValueError(carrier)
