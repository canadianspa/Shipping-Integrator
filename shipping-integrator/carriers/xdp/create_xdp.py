import re
import dicttoxml
import requests

from common.config import XDP_API_URL
from .shared import build_credentials, handle_response


def create_xdp_shipment(carrier, shipment):
    account_no, access_key = build_credentials(carrier)

    # REMOVE WHEN LIVE
    shipment = test_shipment
    xml = build_xml(shipment, "create", account_no, access_key)

    url = XDP_API_URL
    create_resp = requests.post(url, data=xml)
    status, consignment_no, label_url = handle_response(
        create_resp, data=True)

    if status == "OK":
        label_resp = requests.get(label_url)
        label_str = label_resp.content.encode("base64")

        return ({"label": label_str, "tracking_number": consignment_no}, 201)
    else:
        return ({"message": "Error creating consignment"}, 500)


def build_xml(shipment, shimpent_action, account_no, access_key):
    destination = shipment["destination_address"]

    pieces = []
    manifest_weight = 0

    for parcel in shipment["parcels"]:
        manifest_weight += parcel["weight_in_grams"] / 1000

        pieces.append({
            "height": parcel["dimensions"]["height"],
            "width": parcel["dimensions"]["width"],
            "length": parcel["dimensions"]["length"],
        })

    manifest_pieces = len(pieces)

    json = {
        "type": shimpent_action,
        "consignment": {
            "accountno": account_no,
            "accesskey": access_key,
            "references": {
                "ref": "testing comment"
            },
            "deliverycontact": destination["first_name"] + " " + destination["last_name"],
            "deliveryaddress1": destination["line_1"],
            "deliveryaddress2": destination["line_2"],
            "deliverytown": destination["city"],
            "deliverycounty": destination["state"],
            "deliverypostcode": destination["zip"],
            "deliveryphone": destination["phone"],
            "deliveryemail": destination["email"],
            "servicelevel": shipment["service_code"],
            "manifestpieces": manifest_pieces,
            "manifestweight": manifest_weight,
            "label": "yes",
            "dimensions": pieces,
        }
    }

    xml = dicttoxml.dicttoxml(
        json,
        item_func=item_func,
        custom_root="xdpwebservice",
        attr_type=False,
        cdata=True
    )

    # Remove CDATA from <type> tag
    xml_str = xml.decode("utf-8")
    xml_str = xml_str.replace("<type><![CDATA[", "<type>")
    xml_str = xml_str.replace("]]></type>", "</type>")
    xml = xml_str.encode("utf-8")

    return xml


def item_func(x):
    # Name of parent tag for a list item
    return 'piece'


test_shipment = {
    "destination_address":
        {
            "first_name": "TESTING",
            "last_name": "IGNORE",
            "company": "Trotters Independent Traders",
            "city": "Peckham",
            "country": "GB",
            "state": "",
            "zip": "SE15 2EB",
            "phone": "07758989787",
            "email": "sales@trotters.com",
            "line_1": "80 Nelson Mandella House",
            "line_2": "Nyrere Estate"
        },
    "parcels":
        [
            {
                "dimensions": {"height": 15.0, "width": 22.0, "length": 10.0, "unit": "cm"},
                "weight_in_grams": 20000
            }
        ],
    "service_code": "O/N"
}
