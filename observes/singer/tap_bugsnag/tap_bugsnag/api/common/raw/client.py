# Standard libraries
from __future__ import annotations
from typing import (
    Any,
    Callable,
    Dict,
    NamedTuple,
)

# Third party libraries
import requests
from requests.models import Response
from returns.curry import partial

# Local libraries
from tap_bugsnag.api.auth import Credentials


API_URL_BASE = "https://api.bugsnag.com"


def _get(
    creds: Credentials, endpoint: str, params: Dict[str, Any]
) -> Response:
    response = requests.get(
        f"{API_URL_BASE}{endpoint}",
        headers={"Authorization": f"token {creds.api_key}", "X-Version": "2"},
        params=params,
    )
    return response


class Client(NamedTuple):
    get: Callable[[str, Dict[str, Any]], Response]

    @classmethod
    def new(cls, creds: Credentials) -> Client:
        return cls(get=partial(_get, creds))
