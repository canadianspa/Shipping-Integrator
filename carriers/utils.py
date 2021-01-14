import json


def handle_shipment(shipment):
    details = json.loads(shipment["service_code"])
    carrier = details["carrier"]

    shipment["service_code"] = details

    return carrier, shipment


def get_carrier(tracking_number):
    # Get carrier using first char of TrackingNo
    # Z  => XDP
    # L  => DX 1man
    # N/G  => DX 2man

    if tracking_number[0] == "Z":
        return "xdp"
    elif (
        tracking_number[0] == "L"
        or tracking_number[0] == "N"
        or tracking_number[0] == "G"
    ):
        return "dx"
    else:
        raise ValueError(f"Unknown carrier for: {tracking_number}")
