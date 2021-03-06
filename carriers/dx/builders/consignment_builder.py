import time

from common.credentials.logins import DX_ACCOUNT_NUMBER, DX_ORIG_SERVICE_CENTRE


def consignment_builder(shipment):
    manifest_date = int(round(time.time() * 1000))
    
    destination = shipment["destination_address"]
    contents = build_contents(shipment["parcels"])

    consignment = {
        "DXAccountNumber": f"{DX_ACCOUNT_NUMBER}",
        "ManifestDate": f"/Date({manifest_date}+0000)/",
        "ConsignmentReference1": shipment["reference"][1:],
        "OrigServiceCentre": DX_ORIG_SERVICE_CENTRE,
        "ServiceCode": shipment["service_code"]["code"],
        "SpecialInstruction1": "Signature required",
        "DeliveryName": destination["first_name"] + " " + destination["last_name"],
        "DeliveryAddress1": destination["line_1"],
        "DeliveryAddress2": destination["line_2"],
        "DeliveryPostcode": destination["zip"],
        "DeliveryContact": destination["first_name"] + " " + destination["last_name"],
        "DeliveryPhoneNumber": destination["phone"],
        "DeliveryEmail": destination["email"],
        "Contents": contents,
    }

    return consignment


def build_contents(parcels):
    contents = []

    for parcel in parcels:
        contents.append(
            {
                "ContentDescriptionID": 6,
                "ContentDescription": "Pallet",
                "ContentDimension1": int(parcel["dimensions"]["height"]),
                "ContentDimension2": int(parcel["dimensions"]["width"]),
                "ContentDimension3": int(parcel["dimensions"]["length"]),
                "ContentQuantity": 1,
                "ContentTotalWeight": int(parcel["weight_in_grams"] / 1000),
            }
        )

    return contents
