import json


def build_quotes(carrier):
    quotes = [
        build_quote(carrier, "O/N", "Overnight"),
        build_quote(carrier, "ECON", "Economy"),
        build_quote(carrier, "1200", "12pm"),
        build_quote(carrier, "S12", "Sat 12pm"),
        build_quote(carrier, "S10", "Sat 10:30am"),
    ]

    return quotes


def build_quote(carrier, service_code, service_name):
    title = ""
    if carrier == "xdpa":
        title = "XDP A"
    if carrier == "xdpb":
        title = "XDP B"
    if carrier == "xdpc":
        title = "XDP C"

    code = {
        "carrier": carrier,
        "code": service_code,
    }

    quote = {
        "code": json.dumps(code),
        "name": f"{title} - Parcel {service_name}",
        "service_type": "dropoff"
    }

    return quote
