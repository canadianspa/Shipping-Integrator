from carriers.xdp.carrier import build_xdp_quotes
from carriers.dx.carrier import build_dx_quotes


def build_quotes():
    quotes = build_xdp_quotes() + build_dx_quotes()

    return quotes