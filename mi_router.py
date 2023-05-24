import hashlib
import random
import time

import requests
from requests.structures import CaseInsensitiveDict
from urllib3.exceptions import HeaderParsingError


class MiRouter:
    KEY = "a2ffa5c9be07488bbb04a3a47d3c5f6a"

    def __init__(self, gateway_url, token=None):
        self.mac_prefix = "e4:46:da"
        self.token = token
        if not any(i in gateway_url for i in ["http://", "https://"]):
            gateway_url = "http://" + gateway_url
        self.gateway_url = gateway_url
        self.random_mac_address = self.mac_prefix + ":".join("%02x" % random.randint(0, 255) for _ in range(3))
        self.nonce = f"0_{self.random_mac_address}_{int(time.time())}_9999"

    @staticmethod
    def sha1(string):
        """Encode string as UTF-8, and hash it using SHA-1."""
        return hashlib.sha1(string.encode()).hexdigest()

    @staticmethod
    def handle_response(message="", data=None, success=True):
        """Return a dictionary with the keys 'success', 'message', and 'data'."""
        return {"success": success, "message": message, "data": data}

    def handle_get_request(self, url):
        """Get url, append it to the base url, and make a get request to that url."""
        headers = CaseInsensitiveDict()
        headers["Access-Control-Request-Method"] = "GET"
        try:
            req = requests.get(f"{self.get_base_url(with_token=True)}/{url}", headers=headers)
            if req.status_code == 200:
                return self.handle_response(data=req.json())
            return self.handle_response(data=req.content, success=False)
        except HeaderParsingError:
            return self.handle_response(data=req.content, success=False)

    def get_base_url(self, with_token=False):
        """Return a string that is the base URL for the router's web interface"""
        if with_token:
            return f"{self.gateway_url}/cgi-bin/luci/;stok={self.token}"
        return f"{self.gateway_url}/cgi-bin/luci"

    def login(self, password, user="admin"):
        """Get a password and a username, and return a token."""
        url = f"{self.get_base_url()}/api/xqsystem/login"
        req = requests.post(
            url,
            {
                "username": user,
                "password": self.sha1(self.nonce + self.sha1(password + self.KEY)),
                "logtype":  2,
                "nonce":    self.nonce,
            },
        )
        response = req.json()
        if req.status_code == 200 and "token" in response:
            self.token = response["token"]
            return self.handle_response(data=response)
        return self.handle_response(data=req.content, success=False)

    def device_list(self):
        return self.handle_get_request("api/misystem/devicelist")

    def list_devices(self):
        devices = self.handle_get_request("api/misystem/devicelist")
        return [device["mac"] for device in devices["data"]["list"] if device["mac"] != devices["data"]["mac"]]

    def deny_devices(self):
        mac_addresses = self.list_devices()
        for mac in mac_addresses:
            self.handle_get_request(f"api/xqsystem/set_mac_filter?mac={mac}&wan=0")
        return dict(status="OK")

    def allow_devices(self):
        mac_addresses = self.list_devices()
        for mac in mac_addresses:
            self.handle_get_request(f"api/xqsystem/set_mac_filter?mac={mac}&wan=1")
        return dict(status="OK")
