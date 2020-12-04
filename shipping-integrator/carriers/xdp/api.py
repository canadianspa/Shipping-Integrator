import requests
from base64 import b64encode

from common.config import XDP_API_URL
from .utils import handle_response


def create_consignment(xml):
    response = requests.post(XDP_API_URL, data=xml)
    data = handle_response(response, data=True)

    return data


def delete_consignment(xml):
    response = requests.post(XDP_API_URL, data=xml)
    data = handle_response(response)

    return data


def get_label(url):
    response = requests.get(url)

    b64_bytes_str = b64encode(response.content)
    b64_label = b64_bytes_str.decode("utf-8")

    return b64_label
