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
        self.__refresh_session_key()

    def __refresh_session_key(self):
        url = f"{DX_API_URL}/GetSessionKey"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "encoding": "utf-8",
        }

        body = {
            "DXAccountNumber": DX_ACCOUNT_NUMBER,
            "OrigServiceCentre": DX_ORIG_SERVICE_CENTRE,
            "Password": DX_ACCOUNT_PASSWORD,
        }

        response = self.__handle_request(url, body, headers=headers)

        if response["Status"] == 0:
            print("Refreshed DX Session Key")
            self.session_key = response["SessionKey"]
        else:
            raise Exception(f'Session key error: {response["StatusMessage"]}')

    def __handle_request(
        self,
        url,
        body,
        headers=None,
    ):
        headers = headers if headers else {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "encoding": "utf-8",
            "AuthHeader": f"<AuthHeader><SessionKey>{self.session_key}</SessionKey></AuthHeader>"
        }

        data = json.dumps(body)

        response = requests.post(url, data=data, headers=headers)

        return response.json()

    def request(self, url, body):
        response = self.__handle_request(url, body)

        if response["Status"] == 4:
            # Unauthorised
            self.__refresh_session_key()
            return self.request(url, body)
        else:
            return response
