from common.config import XDP_TRACKING_URL

from .api import create_consignment, delete_consignment, get_label

from .utils import build_credentials
from .builders.quotes_builder import build_quotes
from .builders.consignment_builder import build_consignment_xml
from .builders.delete_consignment_builder import build_delete_consignment_xml


def build_xdp_quotes():
    quotes = build_quotes()

    return quotes


def create_xdp_shipment(carrier, shipment):
    account_no, access_key = build_credentials(carrier)

    xml = build_consignment_xml(shipment, "create", account_no, access_key)

    response = create_consignment(xml)

    if response["status"] == "OK":
        label_url = response["label_url"]
        label = get_label(label_url)

        consignment_no = response["consignment_no"]

        return ({"label": label, "tracking_number": consignment_no}, 201)
    else:
        return ({"message": "Error creating consignment"}, 500)


def delete_xdp_shipment(tracking_number):
    account_no, access_key = build_credentials("xdpa")

    xml = build_delete_consignment_xml(access_key, tracking_number)

    response = delete_consignment(xml)

    if response["status"] == "OK":
        return ("", 204)
    else:
        return ("Error deleting consignment", 500)


def redirect_xdp_tracking(tracking_number):
    url = f"{XDP_TRACKING_URL}?c={tracking_number}"

    return url
