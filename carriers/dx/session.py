import requests


class DxSession:
    def __init__(self, ENV, url, account_number, account_password, service_center):
        self.ENV = ENV

        self.url = url
        self.account_number = account_number
        self.account_password = account_password
        self.service_center = service_center

        self.session_key = self.get_session_key()

    def get_session_key(self):
        url = self.url + "/GetSessionKey"

        headers = {
            "Accept": "application/json",
        }

        body = {
            "DXAccountNumber": self.account_number,
            "Password": self.account_password,
            "OrigServiceCentre": self.service_center,
        }

        response = requests.post(url, json=body, headers=headers).json()

        if response["Status"] == 0:
            print(self.ENV + ": Refreshed DX Session Key")
            return response["SessionKey"]
        else:
            raise Exception("ERROR: " + response["StatusMessage"])

    def request(self, url, json):
        headers = {
            "Accept": "application/json",
            "AuthHeader": "<AuthHeader><SessionKey>"
            + self.session_key
            + "</SessionKey></AuthHeader>",
        }

        response = requests.post(url, json=json, headers=headers).json()

        # If unauthorised
        if response["Status"] == 4:
            self.session_key = self.get_session_key()
            return self.request(url, json)
        else:
            return response
