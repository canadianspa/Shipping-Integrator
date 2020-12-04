from .api import (
    create_consignment,
    delete_consignment,
    get_label
)
from .utils import build_credentials
from .builders.quotes_builder import build_quotes
from .builders.consignment_builder import build_consignment_xml
from .builders.delete_consignment_builder import build_delete_consignment_xml


def build_xdp_quotes():
    quotes = build_quotes()

    return quotes, 201


def create_xdp_shipment(carrier, shipment):
    account_no, access_key = build_credentials(carrier)

    xml = build_consignment_xml(
        shipment,
        "create",
        account_no,
        access_key
    )

    response = create_consignment(xml)

    if response.status == "OK":
        label = get_label(response.label_url)

        return ({"label": label, "tracking_number": response.consignment_no}, 201)
    else:
        return ({"message": "Error creating consignment"}, 500)


def delete_xdp_shipment(carrier, tracking_number):
    account_no, access_key = build_credentials(carrier)

    xml = build_delete_consignment_xml(
        access_key,
        tracking_number
    )

    response = delete_consignment(xml)

    if response.status == "OK":
        return ("", 204)
    else:
        return ("Error deleting consignment", 500)
