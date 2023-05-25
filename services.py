from typing import Any, Dict, Optional

import requests
from requests import JSONDecodeError, Response
from requests.structures import CaseInsensitiveDict

from responses import JSONResponse


class RequestService:
    @staticmethod
    def handle_response(response: Response) -> JSONResponse:
        """Unpack response if possible and set its status."""
        try:
            content = response.json()
        except JSONDecodeError:
            content = response.content

        if response.ok:
            return JSONResponse(is_succeeded=True, content=content)
        else:
            return JSONResponse(is_succeeded=False, content=content)

    @classmethod
    def get(
        cls,
        url: str,
        headers: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> JSONResponse:
        """Send GET request and handle response."""

        request_headers = CaseInsensitiveDict()
        request_headers["Access-Control-Request-Method"] = "GET"
        request_headers.update(headers)

        response = requests.get(url=url, headers=request_headers, params=params)
        return cls.handle_response(response)

    @classmethod
    def post(
        cls, url: str, data: Dict[str, Any], headers: Optional[Dict[str, Any]] = None
    ) -> JSONResponse:
        """Send POST request and handle response."""

        request_headers = CaseInsensitiveDict()
        request_headers.update(headers)

        response = requests.post(url=url, headers=request_headers, data=data)
        return cls.handle_response(response)
