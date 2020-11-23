import requests
import dicttoxml

from common.config import XDP_API_URL
from .shared import build_credentials, handle_response


def delete_xdp_shipment(carrier, tracking_number):
    account_no, access_key = build_credentials(carrier)

    json = {
        "type": "delete",
        "accesskey": access_key,
        "consignmentno": tracking_number,
    }

    xml = dicttoxml.dicttoxml(
        json,
        attr_type=False,
        custom_root="xdpwebservice"
    )

    response = requests.post(XDP_API_URL, data=xml)
    status = handle_response(response)

    if status == "OK":
        return ("", 204)
    else:
        return ("Error deleting consignment", 500)
