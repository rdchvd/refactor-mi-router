import json
from typing import Any, Optional


class JSONResponse(dict):
    def __init__(self, is_succeeded: Optional[bool] = False, content: Any = None):
        self.is_succeeded = is_succeeded
        self.content = content
        super().__init__()

    def __repr__(self) -> str:
        """Return a string representation of response that can be used in REST API."""
        return json.dumps({"is_succeeded": self.is_succeeded, "content": self.content})

    @property
    def ok(self) -> bool:
        """Return True if response is successful"""
        return self.is_succeeded
