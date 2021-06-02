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


def parse_tracking_string(tracking_string):
    # Get carrier using first char of TrackingNo
    # Z  => XDP
    # L  => DX 1man
    # N/G  => DX 2man

    if "PANTHER " in tracking_string:
        return "panther", tracking_string.replace("PANTHER ", "")
    elif tracking_string[0] == "Z":
        return "xdp", tracking_string
    elif (
        tracking_string[0] == "L"
        or tracking_string[0] == "N"
        or tracking_string[0] == "G"
    ):
        return "dx", tracking_string
    else:
        raise ValueError("Unknown carrier for: " + tracking_string)
