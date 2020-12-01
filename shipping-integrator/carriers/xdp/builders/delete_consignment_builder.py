from common.utils import json_to_xml


def build_delete_consignment_xml(access_key, tracking_number):
    json = build_delete_consignment_json(access_key, tracking_number)

    xml = json_to_xml(json, custom_root="xdpwebservice",)

    return xml


def build_delete_consignment_json(access_key, tracking_number):
    json = {
        "type": "delete",
        "accesskey": access_key,
        "consignmentno": tracking_number,
    }

    return json
