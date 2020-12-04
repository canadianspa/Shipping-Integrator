import requests
import json
from base64 import b64encode

from common.credentials.logins import (
    DX_ACCOUNT_NUMBER,
    DX_ACCOUNT_PASSWORD,
    DX_ORIG_SERVICE_CENTRE
)
from common.config import DX_API_URL
from .utils import handle_response

headers = {
    "Content-Type": "application/json",
    "encoding": "utf-8",
    "Accept": "application/json"
}


def get_session_key():
    url = f"{DX_API_URL}/GetSessionKey"

    body = {
        "DXAccountNumber": DX_ACCOUNT_NUMBER,
        "OrigServiceCentre": DX_ORIG_SERVICE_CENTRE,
        "Password": DX_ACCOUNT_PASSWORD
    }

    data = json.dumps(body)

    res = requests.post(url, data=data, headers=headers)
    response = handle_response(res)

    return response["SessionKey"]


def create_consignment(body):
    url = f"{DX_API_URL}/AddConsignment"

    data = json.dumps(body)

    res = requests.post(url, data=data, headers=headers)
    response = handle_response(res)

    return response


def delete_consignment(tracking_number):
    url = f"{DX_API_URL}/DeleteConsignment"

    body = {
        "ConsignmentNumber": tracking_number,
        "RoutingStream": "F"
    }

    data = json.dumps(body)

    res = requests.post(url, data=data, headers=headers)
    response = handle_response(res)

    return response
