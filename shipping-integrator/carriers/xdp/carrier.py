import requests

from common.config import XDP_API_URL
from common.utils import class_to_json
from classes.quote import Quote

from .utils import (
    build_credentials,
    handle_response,
    endcode_pdf_string
)
from .builders.consignment_builder import build_consignment_xml
from .builders.delete_consignment_builder import build_delete_consignment_xml


def build_xdp_quotes():
    DROPOFF = "dropoff"

    quotes = [
        Quote("Parcel - Overnight", "O/N", DROPOFF),
        Quote("Parcel - Economy", "ECON", DROPOFF),
        Quote("Parcel - 12pm", "1200", DROPOFF),
        Quote("Parcel - Sat 12pm", "S12", DROPOFF),
        Quote("Parcel - Sat 10.30am", "S10", DROPOFF),
    ]

    return class_to_json(quotes), 201


def create_xdp_shipment(carrier, shipment):
    account_no, access_key = build_credentials(carrier)

    xml = build_consignment_xml(
        shipment,
        "create",
        account_no,
        access_key
    )

    response = requests.post(XDP_API_URL, data=xml)
    response_data = handle_response(response, data=True)

    if response_data.status == "OK":
        response = requests.get(response_data.label_url)
        b64_str = endcode_pdf_string(response.content)

        return ({"label": b64_str, "tracking_number": response_data.consignment_no}, 201)
    else:
        return ({"message": "Error creating consignment"}, 500)


def delete_xdp_shipment(carrier, tracking_number):
    account_no, access_key = build_credentials(carrier)

    xml = build_delete_consignment_xml(access_key, tracking_number)

    response = requests.post(XDP_API_URL, data=xml)
    response_data = handle_response(response)

    if response_data.status == "OK":
        return ("", 204)
    else:
        return ("Error deleting consignment", 500)
