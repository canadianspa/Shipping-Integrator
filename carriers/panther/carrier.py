from flask import jsonify, redirect
import requests
from base64 import b64encode
from datetime import datetime, timedelta

from common.credentials import PANTHER_API_KEY_TEST, PANTHER_API_KEY_LIVE
from ..utils import build_quote


class Panther:
    def __init__(self, testing):
        self.ENV = "TEST" if testing else "LIVE"

        if testing:
            self.api_key = PANTHER_API_KEY_TEST
            self.url = "https://api-staging.panthergroup.co.uk/apiv2/public"
        else:
            self.api_key = PANTHER_API_KEY_LIVE
            self.url = "https://api.panthergroup.co.uk/apiv2/public"

        self.tracking_url = "https://pgtrack.com/"

        print(self.ENV + ": Panther initialised")

    def quotes(self):
        return [
            build_quote("panther", 1, "Panther - 1man Delivery (2 days)"),
            build_quote("panther", 2, "Panther - 2man Delivery (2 days)"),
            build_quote("panther", 3, "Panther - 3man Delivery (2 days)"),
        ]

    def create(self, service_type, shipment):
        consignmentno = shipment["reference"].replace("#", "")
        deliverydate = datetime.today() + timedelta(days=2)

        body = {
            "key": self.api_key,
            "consignmentno": consignmentno,
            "deliveryname": f'{shipment["destination_address"]["first_name"]} {shipment["destination_address"]["last_name"]}',
            "deliveryaddress1": shipment["destination_address"]["line_1"],
            "deliveryaddress2": shipment["destination_address"]["line_2"],
            "deliverypostcode": shipment["destination_address"]["zip"],
            "deliverytelephone1": shipment["destination_address"]["phone"],
            "deliveryemail": shipment["destination_address"]["email"],
            "deliverydate": deliverydate.strftime("%d/%m/%Y"),
            "servicetype": service_type,
            "lines": [
                {
                    "suppliername": "canadianspa",
                    "productcode": "Canadian Spa Company",
                    "productdescription": "N/a",
                    "noofitems": 1,
                    "weight": parcel["weight_in_grams"] / 1000,
                    "height": parcel["dimensions"]["height"],
                    "width": parcel["dimensions"]["width"],
                    "depth": parcel["dimensions"]["length"],
                }
                for parcel in shipment["parcels"]
            ],
            "json": 1,
        }

        url = self.url + "/create_order"

        response = requests.post(url, json=body)

        if response.status_code == 200:
            response = {
                "label": self.get_label(consignmentno),
                "tracking_number": "PANTHER " + consignmentno,
            }

            return jsonify(response), 201
        else:
            return "Consignment not created", 500

    def delete(self, consignmentno):
        url = self.url + "/delete_order"

        body = {
            "key": self.api_key,
            "order": consignmentno,
            "json": 1,
        }

        response = requests.post(url, json=body)

        if response.status_code == 200:
            return "Consignment deleted", 204
        else:
            return "Consignment not deleted", 500

    def track(self, consignmentno):
        url = self.tracking_url + consignmentno

        return redirect(url, code=302)

    def get_label(self, consignmentno):
        url = self.url + "/order/labels"

        body = {
            "key": self.api_key,
            "orderno": consignmentno,
            "format": "pdf",
            "json": 1,
        }

        response = requests.post(url, json=body)

        return b64encode(response.content).decode("utf-8")