def build_consignment(account_number, access_key, service_code, shipment):
    pieces, weight = build_pieces(shipment)

    return f"""
    <?xml version="1.0" encoding="UTF-8" ?>
    <xdpwebservice>
        <type>{"create"}</type>
        <consignment>
            <accountno><![CDATA[{account_number}]]></accountno>
            <accesskey><![CDATA[{access_key}]]></accesskey>
            <references>
                <ref><![CDATA[{shipment["reference"]}]]></ref>
            </references>
            <deliverycontact><![CDATA[{shipment["destination_address"]["first_name"]} {shipment["destination_address"]["last_name"]}]]></deliverycontact>
            <deliveryaddress1><![CDATA[{shipment["destination_address"]["line_1"]}]]></deliveryaddress1>
            <deliveryaddress2><![CDATA[{shipment["destination_address"]["line_2"]}]]></deliveryaddress2>
            <deliverytown><![CDATA[{shipment["destination_address"]["city"]}]]></deliverytown>
            <deliverycounty><![CDATA[{shipment["destination_address"]["state"]}]]></deliverycounty>
            <deliverypostcode><![CDATA[{shipment["destination_address"]["zip"]}]]></deliverypostcode>
            <deliveryphone><![CDATA[{shipment["destination_address"]["phone"]}]]></deliveryphone>
            <deliveryemail><![CDATA[{shipment["destination_address"]["email"]}]]></deliveryemail>
            <deliverynotes><![CDATA[{"Signature required"}]]></deliverynotes>
            <servicelevel><![CDATA[{service_code}]]></servicelevel>
            <manifestweight><![CDATA[{weight}]]></manifestweight>
            <manifestpieces><![CDATA[{len(pieces)}]]></manifestpieces>
            <label><![CDATA[{"yes"}]]></label>
            <pieces>{"".join(pieces)}</pieces>
        </consignment>
    </xdpwebservice>
    """


def build_pieces(shipment):
    pieces = []
    weight = 0

    for parcel in shipment["parcels"]:
        pieces.append(
            f"""
            <piece>
                <height><![CDATA[{parcel["dimensions"]["height"]}]]></height>
                <width><![CDATA[{parcel["dimensions"]["width"]}]]></width>
                <length><![CDATA[{parcel["dimensions"]["length"]}]]></length>
            </piece>
        """
        )
        weight += int(parcel["weight_in_grams"] / 1000)

    return pieces, weight