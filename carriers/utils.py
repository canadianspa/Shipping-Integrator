import json
import requests


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
    """
    Get carrier using first char of TrackingNo
    :param Z  => XDP
    :param L  => DX 1man
    :param N/G  => DX 2man
    """

    tracking_string = requests.utils.unquote(tracking_string)

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
