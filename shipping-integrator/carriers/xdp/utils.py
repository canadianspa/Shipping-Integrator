import dicttoxml
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


def build_xml(shipment, shimpent_action, account_no, access_key):
    destination = shipment["destination_address"]

    pieces, manifest_weight = build_pieces(shipment["parcels"])

    json = {
        "type": shimpent_action,
        "consignment": {
            "accountno": account_no,
            "accesskey": access_key,
            "references": {
                "ref": shipment["reference"]
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
            "manifestweight": manifest_weight,
            "manifestpieces": len(pieces),
            "label": "yes",
            "pieces": pieces,
        }
    }

    # Name of parent tag for a list item
    def item_func(x): return 'piece'

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


def build_pieces(parcels):
    pieces = []
    weight = 0

    for parcel in parcels:
        pieces.append({
            "height": parcel["dimensions"]["height"],
            "width": parcel["dimensions"]["width"],
            "length": parcel["dimensions"]["length"],
        })

        weight += int(parcel["weight_in_grams"] / 1000)

    return pieces, weight
