from flask import redirect, jsonify
from base64 import b64encode
import requests
import xml.etree.ElementTree as ET

from common.credentials import (
    XDP_A_NUMBER,
    XDP_B_NUMBER,
    XDP_C_NUMBER,
    XDP_A_KEY,
    XDP_B_KEY,
    XDP_C_KEY,
)
from ..utils import build_quote
from .builder import build_consignment


class XDP:
    def __init__(self, testing=True):
        self.ENV = "TEST" if testing else "LIVE"

        self.url = "https://xdp.sysx.co.uk/api/webservice/rest/endpoint"
        self.tracking_url = "https://www.xdp.co.uk/track.php"

        print(self.ENV + ": XDP initialised")

    def quotes(self):
        def build_quotes_wrapper(carrier, title):
            return [
                build_quote(carrier, "O/N", f"{title} - Overnight"),
                build_quote(carrier, "ECON", f"{title} - Economy"),
                build_quote(carrier, "1200", f"{title} - 12pm"),
                build_quote(carrier, "S12", f"{title} - Sat 12pm"),
                build_quote(carrier, "S10", f"{title} - Sat 10:30am"),
            ]

        return (
            build_quotes_wrapper("xdpa", "XDP A")
            + build_quotes_wrapper("xdpb", "XDP B")
            + build_quotes_wrapper("xdpc", "XDP C")
        )

    def create(self, carrier, service_code, shipment):
        account_no, access_key = self.get_credentials(carrier)

        data = build_consignment(
            account_no,
            access_key,
            service_code,
            shipment,
        )

        response = requests.post(self.url, data=data)

        xml = ET.fromstring(response.content)

        if xml.find(".//valid").text == "OK":
            consignment_no = xml.find(".//consignmentno").text
            label_url = xml.find(".//label").text

            response = {
                "label": self.get_label(label_url),
                "tracking_number": consignment_no,
            }

            return jsonify(response), 201
        else:
            return "Consignment not created", 500

    def delete(self, consignmentno):
        account_no, access_key = self.get_credentials("xdpa")

        data = f"""
            <?xml version="1.0" encoding="UTF-8" ?>
            <xdpwebservice>
                <type>{"delete"}</type>
                <accesskey>{access_key}</accesskey>
                <consignmentno>{consignmentno}</consignmentno>
            </xdpwebservice>
        """

        response = requests.post(self.url, data=data)

        xml = ET.fromstring(response.content)

        if xml.find(".//valid").text == "OK":
            return "Consignment deleted", 204
        else:
            return "Consignment not deleted", 500

    def track(self, consignmentno):
        url = f"{self.tracking_url}?c={consignmentno}"

        return redirect(url, code=302)

    def get_label(self, url):
        response = requests.get(url)

        return b64encode(response.content).decode("utf-8")

    def get_credentials(self, carrier):
        if carrier == "xdpa":
            return XDP_A_NUMBER, XDP_A_KEY
        elif carrier == "xdpb":
            return XDP_B_NUMBER, XDP_B_KEY
        elif carrier == "xdpc":
            return XDP_C_NUMBER, XDP_C_KEY
        else:
            raise ValueError(carrier)