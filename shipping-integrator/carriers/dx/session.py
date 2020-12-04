import requests
import json

from common.credentials.logins import (
    DX_ACCOUNT_NUMBER,
    DX_ACCOUNT_PASSWORD,
    DX_ORIG_SERVICE_CENTRE,
)
from common.config import DX_API_URL


class DxSession:
    def __init__(self):
        self.refresh_key()

    def refresh_key(self):
        url = f"{DX_API_URL}/GetSessionKey"

        body = {
            "DXAccountNumber": DX_ACCOUNT_NUMBER,
            "OrigServiceCentre": DX_ORIG_SERVICE_CENTRE,
            "Password": DX_ACCOUNT_PASSWORD,
        }

        response = self.handle_request(url, body, use_session_key=False)

        self.session_key = response["SessionKey"]

    def handle_request(self, url, body, use_session_key=True):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "encoding": "utf-8",
        }

        if use_session_key:
            headers[
                "AuthHeader"
            ] = f"<AuthHeader><SessionKey>{self.session_key}</SessionKey></AuthHeader>"

        data = json.dumps(body)

        res = requests.post(url, data=data, headers=headers)
        response = self.handle_response(res)

        # If status == 4 (unauthorized) => refresh token
        if response["Status"] == 4:
            self.refresh_key()
            return self.handle_request(url, body)

        return response

    def handle_response(self, response):
        response = response.json()

        if response["Status"] == 0:
            return response
        else:
            print(response["StatusMessage"])
            return response