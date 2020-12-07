from common.utils import json_to_xml


def build_consignment_xml(shipment, shimpent_type, account_no, access_key):
    json = build_consignment_json(
        shipment, shimpent_type, account_no, access_key)

    xml = json_to_xml(json, custom_root="xdpwebservice", cdata=True)

    # Remove CDATA from <type> tag
    xml_str = xml.decode("utf-8")
    xml_str = xml_str.replace("<type><![CDATA[", "<type>")
    xml_str = xml_str.replace("]]></type>", "</type>")
    xml = xml_str.encode("utf-8")

    return xml


def build_consignment_json(shipment, shimpent_type, account_no, access_key):
    destination = shipment["destination_address"]

    pieces, manifest_weight = build_pieces_json(shipment["parcels"])

    json = {
        "type": shimpent_type,
        "consignment": {
            "accountno": account_no,
            "accesskey": access_key,
            "references": {"ref": shipment["reference"]},
            "deliverycontact": destination["first_name"]
            + " "
            + destination["last_name"],
            "deliveryaddress1": destination["line_1"],
            "deliveryaddress2": destination["line_2"],
            "deliverytown": destination["city"],
            "deliverycounty": destination["state"],
            "deliverypostcode": destination["zip"],
            "deliveryphone": destination["phone"],
            "deliveryemail": destination["email"],
            "deliverynotes": "Signature required",
            "servicelevel": shipment["service_code"]["code"],
            "manifestweight": manifest_weight,
            "manifestpieces": len(pieces),
            "label": "yes",
            "pieces": pieces,
        },
    }

    return json


def build_pieces_json(parcels):
    pieces = []
    weight = 0

    for parcel in parcels:
        pieces.append(
            {
                "height": parcel["dimensions"]["height"],
                "width": parcel["dimensions"]["width"],
                "length": parcel["dimensions"]["length"],
            }
        )

        weight += int(parcel["weight_in_grams"] / 1000)

    return pieces, weight
