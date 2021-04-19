# Standard libraries
from __future__ import (
    annotations,
)
from typing import (
    Any,
    Callable,
    NamedTuple,
)

# Third party libraries
import requests
from returns.curry import (
    partial,
)

# Local libraries
from tap_checkly.api.auth import (
    Credentials,
)


API_URL_BASE = 'https://api.checklyhq.com'


def _get(creds: Credentials, endpoint: str, **kwargs: Any) -> Any:
    response = requests.get(
        f'{API_URL_BASE}{endpoint}',
        headers={'Authorization': f'Bearer {creds.api_key}'},
        **kwargs
    )
    response.raise_for_status()
    return response.json()


class Client(NamedTuple):
    get: Callable[..., Any]

    @classmethod
    def new(cls, creds: Credentials) -> Client:
        return cls(
            get=partial(_get, creds)
        )
