from builders.quote import build_quote


def build_quotes():
    quotes = (
        build_quotes_wrapper("xdpa", "XDP A")
        + build_quotes_wrapper("xdpb", "XDP B")
        + build_quotes_wrapper("xdpc", "XDP C")
    )

    return quotes


def build_quotes_wrapper(carrier, title):
    quotes = [
        build_quote(carrier, "O/N", f"{title} - Overnight"),
        build_quote(carrier, "ECON", f"{title} - Economy"),
        build_quote(carrier, "1200", f"{title} - 12pm"),
        build_quote(carrier, "S12", f"{title} - Sat 12pm"),
        build_quote(carrier, "S10", f"{title} - Sat 10:30am"),
    ]

    return quotes
