from common.config import DX_API_URL
from .session import DxSession

session = DxSession()


def create_consignment(body):
    url = f"{DX_API_URL}/AddConsignment"

    response = session.handle_request(url, body)

    return response


def delete_consignment(tracking_number):
    url = f"{DX_API_URL}/DeleteConsignment"

    body = {
        "ConsignmentNumber": tracking_number,
        "RoutingStream": "F",
    }

    response = session.handle_request(url, body)

    return response


def get_labels(consignment_number):
    url = f"{DX_API_URL}/GetLabels"

    body = {
        "ConsignmentNumber": consignment_number,
        "LabelReturnType": 0,
        "PDFLabelConfig": {"labelSetup": 1, "startingPosition": 1},
        "PrintSelection": 0,
        "RoutingStream": "F",
    }

    response = session.handle_request(url, body)

    return response["label"]