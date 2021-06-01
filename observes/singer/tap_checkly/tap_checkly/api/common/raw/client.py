from __future__ import (
    annotations,
)

import requests
from returns.curry import (
    partial,
)
from tap_checkly.api.common.raw.auth import (
    Credentials,
)
from typing import (
    Any,
    Callable,
    NamedTuple,
)

API_URL_BASE = "https://api.checklyhq.com"


def _get(creds: Credentials, endpoint: str, **kwargs: Any) -> Any:
    response = requests.get(
        f"{API_URL_BASE}{endpoint}",
        headers={"Authorization": f"Bearer {creds.api_key}"},
        **kwargs,
    )
    response.raise_for_status()
    return response.json()


class Client(NamedTuple):
    get: Callable[..., Any]

    @classmethod
    def new(cls, creds: Credentials) -> Client:
        return cls(get=partial(_get, creds))
