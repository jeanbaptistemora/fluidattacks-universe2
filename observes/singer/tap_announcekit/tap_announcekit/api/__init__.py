from dataclasses import (
    dataclass,
)
from sgqlc.endpoint.http import (
    HTTPEndpoint,
)
from tap_announcekit.api.auth import (
    Creds,
)

API_ENDPOINT = "https://announcekit.app/gq/v2"


@dataclass(frozen=True)
class _ApiClient:
    endpoint: HTTPEndpoint


class ApiClient(_ApiClient):
    # pylint: disable=too-few-public-methods
    def __init__(self, creds: Creds) -> None:
        obj = _ApiClient(HTTPEndpoint(API_ENDPOINT, creds.basic_auth_header()))
        for key, val in obj.__dict__.items():
            object.__setattr__(self, key, val)


__all__ = [
    "Creds",
]
