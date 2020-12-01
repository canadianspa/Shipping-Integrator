from base64 import b64encode
import xml.etree.ElementTree as ET

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


def build_credentials(carrier):
    if carrier == "xdpa":
        return XDP_A_NUMBER, XDP_A_KEY
    elif carrier == "xdpb":
        return XDP_B_NUMBER, XDP_B_KEY
    elif carrier == "xdpc":
        return XDP_C_NUMBER, XDP_C_KEY
    else:
        raise ValueError(carrier)


class Resp():
    status = None
    consignment_no = None
    label_url = None


def handle_response(response, data=False):
    resp = Resp()

    xml = ET.fromstring(response.content)
    resp.status = xml.find('.//valid').text

    if data and resp.status == "OK":
        resp.consignment_no = xml.find('.//consignmentno').text
        resp.label_url = xml.find('.//label').text

        return resp
    else:
        return resp


def endcode_pdf_string(string):
    b64_bytes_str = b64encode(string)
    b64_str = b64_bytes_str.decode("utf-8")

    return b64_str
