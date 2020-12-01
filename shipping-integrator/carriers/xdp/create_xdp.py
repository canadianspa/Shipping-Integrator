import requests
from base64 import b64encode

from common.config import XDP_API_URL
from .utils import (
    build_credentials,
    handle_response,
    build_xml
)


def create_xdp_shipment(carrier, shipment):
    account_no, access_key = build_credentials(carrier)

    xml = build_xml(shipment, "create", account_no, access_key)
    response = requests.post(XDP_API_URL, data=xml)

    status, consign_no, label_url = handle_response(response, data=True)

    if status == "OK":
        response = requests.get(label_url)

        b64_bytes_str = b64encode(response.content)
        b64_str = b64_bytes_str.decode("utf-8")

        return ({"label": b64_str, "tracking_number": consign_no}, 201)
    else:
        return ({"message": "Error creating consignment"}, 500)
