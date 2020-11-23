import re
import dicttoxml
import requests

from common.config import XDP_API_URL
from .shared import build_credentials, handle_response


def create_xdp_shipment(carrier, shipment):
    account_no, access_key = build_credentials(carrier)

    xml = build_xml(shipment, "create", account_no, access_key)

    create_resp = requests.post(XDP_API_URL, data=xml)
    status, consign_no, label_url = handle_response(create_resp, data=True)

    if status == "OK":
        label_resp = requests.get(label_url)
        label_str = label_resp.content.encode("base64")

        return ({"label": label_str, "tracking_number": consign_no}, 201)
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
