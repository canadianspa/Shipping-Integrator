import json


def build_quote(carrier, service_code, title):
    code = {
        "carrier": carrier,
        "code": service_code,
    }

    quote = {
        "code": json.dumps(code),
        "name": title,
        "service_type": "dropoff",
    }

    return quote