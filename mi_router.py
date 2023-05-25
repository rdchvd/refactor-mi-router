import hashlib
import random
import time
from typing import List, Optional

from responses import JSONResponse
from services import RequestService
from settings import (
    ALLOW_MAC_URL_ENDPOINT,
    BASE_URL_ENDPOINT,
    BASE_URL_WITH_TOKEN_ENDPOINT,
    DEFAULT_MAC_PREFIX,
    DENY_MAC_URL_ENDPOINT,
    GET_DEVICE_LIST_URL_ENDPOINT,
    LOGIN_URL_ENDPOINT,
    SECRET_KEY,
)


class MiRouter:
    def __init__(self, gateway_url: str, token=None):
        self.token = token
        self.gateway_url = self.fix_gateway_url(gateway_url)
        self.random_mac_address = self.get_random_mac()
        self.nonce = self.get_random_nonce()

    @staticmethod
    def fix_gateway_url(gateway_url: str) -> str:
        """Add http suffix to url to make it valid."""
        if not gateway_url.startswith(("http://", "https://")):
            gateway_url = "http://" + gateway_url
        return gateway_url

    @staticmethod
    def get_random_mac() -> str:
        """Return a random MAC address."""
        random_numbers = ":".join(f"{random.randint(0, 255):02x}" for _ in range(3))
        return DEFAULT_MAC_PREFIX + ":" + random_numbers

    def get_random_nonce(self) -> str:
        """Get nonce for random mac address."""
        return f"0_{self.random_mac_address}_{int(time.time())}_9999"

    @staticmethod
    def sha1(string) -> str:
        """Encode string as UTF-8, and hash it using SHA-1."""
        return hashlib.sha1(string.encode()).hexdigest()

    @property
    def base_url(self) -> str:
        """Return base URL for the router's web interface."""
        return self.gateway_url + BASE_URL_ENDPOINT

    @property
    def base_url_with_token(self) -> str:
        """Return base URL for the router's web interface with token."""
        if not self.token:
            return self.base_url
        return self.gateway_url + BASE_URL_WITH_TOKEN_ENDPOINT.format(token=self.token)

    def get_encoded_password(self, password) -> str:
        """Encode password to make it valid for API."""
        return self.sha1(self.nonce + self.sha1(password + SECRET_KEY))

    def send_login_request(self, username: str, password: str) -> JSONResponse:
        """Send a login request."""
        return RequestService.post(
            url=self.base_url + LOGIN_URL_ENDPOINT,
            data={
                "username": username,
                "password": self.get_encoded_password(password),
                "logtype": 2,
                "nonce": self.nonce,
            },
        )

    def login(self, username: str, password: str) -> JSONResponse:
        """Get a password and a username, and set a token."""
        response = self.send_login_request(username, password)
        if response.is_succeeded:
            self.token = response.content["token"]
        return response

    def get_full_devices_info(self) -> JSONResponse:
        """Select all connected to router devices."""
        return RequestService.get(
            self.base_url_with_token + GET_DEVICE_LIST_URL_ENDPOINT
        )

    def get_connected_mac_addresses(self) -> Optional[List[str]]:
        """Get connected to router mac addresses except admin one."""
        devices_response = self.get_full_devices_info()
        if not devices_response.is_succeeded:
            return []
        current_device_mac = devices_response.content["mac"]
        devices = devices_response.content["list"]
        return [
            device["mac"] for device in devices if device["mac"] != current_device_mac
        ]

    def send_request_for_all_devices(self, url: str) -> JSONResponse:
        """Send get request to all mac devices."""
        if url not in [DENY_MAC_URL_ENDPOINT, ALLOW_MAC_URL_ENDPOINT]:
            raise NotImplementedError

        mac_addresses = self.get_connected_mac_addresses()
        for mac in mac_addresses:
            response = RequestService.get(
                self.base_url_with_token + url.format(mac=mac)
            )

            if not response.is_succeeded:
                return JSONResponse(is_succeeded=False)

        return JSONResponse(is_succeeded=True)

    def deny_network_for_all_devices(self) -> JSONResponse:
        """Remove network connection for all connected to router devices."""
        return self.send_request_for_all_devices(DENY_MAC_URL_ENDPOINT)

    def allow_network_for_all_devices(self) -> JSONResponse:
        """Allow network connection to all connected to router devices."""
        return self.send_request_for_all_devices(ALLOW_MAC_URL_ENDPOINT)
