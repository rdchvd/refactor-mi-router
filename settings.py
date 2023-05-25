import os

SECRET_KEY = os.getenv("SECRET_KEY")
DEFAULT_MAC_PREFIX = os.getenv("DEFAULT_MAC_PREFIX", "e4:46:da")
BASE_URL_ENDPOINT = os.getenv("BASE_URL_ENDPOINT", "/cgi-bin/luci")
BASE_URL_WITH_TOKEN_ENDPOINT = os.getenv(
    "BASE_URL_WITH_TOKEN_ENDPOINT", "/cgi-bin/luci/;stok={token}"
)
LOGIN_URL_ENDPOINT = os.getenv("LOGIN_URL_ENDPOINT", "/api/xqsystem/login")
GET_DEVICE_LIST_URL_ENDPOINT = os.getenv(
    "GET_DEVICE_LIST_URL_ENDPOINT", "/api/misystem/devicelist"
)
DENY_MAC_URL_ENDPOINT = os.getenv(
    "DENY_MAC_URL_ENDPOINT", "/api/xqsystem/set_mac_filter?mac={mac}&wan=0"
)
ALLOW_MAC_URL_ENDPOINT = os.getenv(
    "ALLOW_MAC_URL_ENDPOINT", "/api/xqsystem/set_mac_filter?mac={mac}&wan=1"
)
