from common.config import (
    XDP_A_NUMBER,
    XDP_B_NUMBER,
    XDP_C_NUMBER,
)
from common.credentials.keys import (
    XDP_A_KEY,
    XDP_B_KEY,
    XDP_C_KEY
)

import xml.etree.ElementTree as ET


def build_credentials(carrier):
    if carrier == "xdpa":
        return XDP_A_NUMBER, XDP_A_KEY
    elif carrier == "xdpb":
        return XDP_B_NUMBER, XDP_B_KEY
    elif carrier == "xdpc":
        return XDP_C_NUMBER, XDP_C_KEY
    else:
        raise ValueError(carrier)


def handle_response(response, data=False):
    xml = ET.fromstring(response.content)
    status = xml.find('.//valid').text

    if data:
        consignment_no = None
        label_url = None

        if status == "OK":
            consignment_no = xml.find('.//consignmentno').text
            label_url = xml.find('.//label').text

        return status, consignment_no, label_url
    else:
        return status
