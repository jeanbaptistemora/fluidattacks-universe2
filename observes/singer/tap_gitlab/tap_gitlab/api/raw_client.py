from __future__ import (
    annotations,
)

import requests
from requests.models import (
    Response,
)
from returns.io import (
    IO,
)
from tap_gitlab.api.auth import (
    Credentials,
)
from typing import (
    Any,
    Dict,
    NamedTuple,
)

API_URL_BASE = "https://gitlab.com/api/v4/projects"


class RawClient(NamedTuple):
    creds: Credentials

    def get(self, endpoint: str, params: Dict[str, Any]) -> IO[Response]:
        response = requests.get(
            "".join([API_URL_BASE, endpoint]),
            headers={"Private-Token": self.creds.api_key},
            params=params,
        )
        return IO(response)
