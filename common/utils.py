import json
import dicttoxml


def handle_shipment(shipment):
    details = json.loads(shipment["service_code"])
    carrier = details["carrier"]

    shipment["service_code"] = details

    return carrier, shipment


def get_carrier(tracking_number):
    if tracking_number[0] == "Z":
        return "xdp"
    elif tracking_number[0] == "L" or tracking_number[0] == "P":
        return "dx"
    else:
        raise ValueError(f"Unknown carrier for: {tracking_number}")


def json_to_xml(json, custom_root, cdata=False):
    # Name of parent tag for a list item
    def item_func(x):
        return "piece"

    xml = dicttoxml.dicttoxml(
        json,
        item_func=item_func,
        custom_root=custom_root,
        attr_type=False,
        cdata=cdata,
    )

    return xml


def class_to_json(classes):
    string = json.dumps(classes, default=lambda o: o.__dict__)
    return json.loads(string)
