from common.config import DX_API_URL


def create_consignment(session, body):
    url = f"{DX_API_URL}/AddConsignment"

    response = session.request(url, body)

    return response


def delete_consignment(session, tracking_number):
    url = f"{DX_API_URL}/DeleteConsignment"

    body = {
        "ConsignmentNumber": tracking_number,
        "RoutingStream": "F",
    }

    response = session.request(url, body)

    return response


def get_labels(session, consignment_number):
    url = f"{DX_API_URL}/GetLabels"

    body = {
        "ConsignmentNumber": consignment_number,
        "LabelReturnType": 0,
        "PDFLabelConfig": {"labelSetup": 2, "startingPosition": 1},
        "PrintSelection": 2,
        "RoutingStream": "F",
    }

    response = session.request(url, body)

    return response["label"]
