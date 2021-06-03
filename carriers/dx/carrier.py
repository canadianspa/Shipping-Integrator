from flask import redirect, jsonify
import time

from ..utils import build_quote
from common.credentials import (
    DX_ACCOUNT_NUMBER_LIVE,
    DX_ACCOUNT_PASSWORD_LIVE,
    DX_ORIG_SERVICE_CENTRE_LIVE,
    DX_ACCOUNT_NUMBER_TEST,
    DX_ACCOUNT_PASSWORD_TEST,
    DX_ORIG_SERVICE_CENTRE_TEST,
)

from .session import DxSession


class DX:
    def __init__(self, testing):
        self.ENV = "TEST" if testing else "LIVE"

        if testing:
            self.account_number = DX_ACCOUNT_NUMBER_TEST
            self.account_password = DX_ACCOUNT_PASSWORD_TEST
            self.service_center = DX_ORIG_SERVICE_CENTRE_TEST
            self.url = "http://itd.dx-track.com/DespatchManager.API.Service.DM6Lite_Test/DM6LiteService.svc"
        else:
            self.account_number = DX_ACCOUNT_NUMBER_LIVE
            self.account_password = DX_ACCOUNT_PASSWORD_LIVE
            self.service_center = DX_ORIG_SERVICE_CENTRE_LIVE
            self.url = "https://dx-track.com/DespatchManager.API.Service.DM6Lite/DM6LiteService.svc"

        self.tracking_url = "https://www.dxdelivery.com/consumer/my-tracking/"

        self.session = DxSession(
            self.ENV,
            self.url,
            self.account_number,
            self.account_password,
            self.service_center,
        )

        print(self.ENV + ": DX initialised")

    def quotes(self):
        return [
            build_quote("dx", "H2", "DX 2man - Standard"),
            build_quote("dx", "H1", "DX 2man - Overnight"),
            build_quote("dx", "HS", "DX 2man - Saturday"),
        ]

    def create(self, service_code, shipment):
        manifest_date = int(round(time.time() * 1000))

        body = {
            "DXAccountNumber": self.account_number,
            "ManifestDate": f"/Date({manifest_date}+0000)/",
            "ConsignmentReference1": shipment["reference"].replace("#", ""),
            "OrigServiceCentre": self.service_center,
            "ServiceCode": service_code,
            "SpecialInstruction1": "Signature required",
            "DeliveryName": f'{shipment["destination_address"]["first_name"]} {shipment["destination_address"]["last_name"]}',
            "DeliveryAddress1": shipment["destination_address"]["line_1"],
            "DeliveryAddress2": shipment["destination_address"]["line_2"],
            "DeliveryPostcode": shipment["destination_address"]["zip"],
            "DeliveryContact": f'{shipment["destination_address"]["first_name"]} {shipment["destination_address"]["last_name"]}',
            "DeliveryPhoneNumber": shipment["destination_address"]["phone"],
            "DeliveryEmail": shipment["destination_address"]["email"],
            "Contents": [
                {
                    "ContentDescriptionID": 6,
                    "ContentDescription": "Pallet",
                    "ContentDimension1": int(parcel["dimensions"]["height"]),
                    "ContentDimension2": int(parcel["dimensions"]["width"]),
                    "ContentDimension3": int(parcel["dimensions"]["length"]),
                    "ContentQuantity": 1,
                    "ContentTotalWeight": int(parcel["weight_in_grams"] / 1000),
                }
                for parcel in shipment["parcels"]
            ],
        }

        url = self.url + "/AddConsignment"

        response = self.session.request(url, body)

        if response["Status"] == 0:
            consignmentno = response["ConsignmentNumber"]

            response = {
                "label": self.get_label(consignmentno),
                "tracking_number": consignmentno,
            }

            return jsonify(response), 201
        else:
            print("ERROR: ", response)
            return "Consignment not created", 500

    def delete(self, consignmentno):
        url = self.url + "/DeleteConsignment"

        body = {
            "ConsignmentNumber": consignmentno,
            "RoutingStream": "F",
        }

        response = self.session.request(url, body)

        if response["Status"] == 0:
            return "Consignment deleted", 204
        else:
            print("ERROR: ", response)
            return "Consignment not deleted", 500

    def track(self, consignmentno):
        url = self.tracking_url

        return redirect(url, code=302)

    def get_label(self, consignmentno):
        url = self.url + "/GetLabels"

        body = {
            "ConsignmentNumber": consignmentno,
            "LabelReturnType": 0,
            "PDFLabelConfig": {
                "labelSetup": 2,
                "startingPosition": 1,
            },
            "PrintSelection": 2,
            "RoutingStream": "F",
        }

        response = self.session.request(url, body)

        return response["label"]
