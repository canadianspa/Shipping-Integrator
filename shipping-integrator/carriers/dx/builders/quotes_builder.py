import json


def build_quotes(carrier):
    quotes = [
        build_quote(carrier, "1man", "ON", "Overnight"),
        build_quote(carrier, "1man", "930", "Overnight 9:30"),
        build_quote(carrier, "1man", "AM", "Overnight pre-noon"),
        build_quote(carrier, "1man", "3Day", "3Day"),
        build_quote(carrier, "1man", "SAT", "Saturday"),
        build_quote(carrier, "1man", "S93", "Saturday 9:30"),
        build_quote(carrier, "2man", "H2", "Standard"),
        build_quote(carrier, "2man", "H1", "Overnight"),
        build_quote(carrier, "2man", "HS", "Saturday"),
        build_quote(carrier, "2man", "C1", "Collection Overnight"),
        build_quote(carrier, "2man", "C2", "Collection Standard"),
        build_quote(carrier, "2man", "CS", "Collection Saturday"),
    ]

    return quotes


def build_quote(carrier, prefix, service_code, service_name):
    code = {
        "carrier": carrier,
        "code": service_code,
    }

    quote = {
        "code": json.dumps(code),
        "name": f"DX {prefix} - {service_name}",
        "service_type": "dropoff"
    }

    return quote
