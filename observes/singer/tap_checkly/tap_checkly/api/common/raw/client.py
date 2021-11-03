from __future__ import (
    annotations,
)

import logging
import requests  # type: ignore
from returns.curry import (
    partial,
)
from singer_io.singer2.json import (
    JsonFactory,
    JsonObj,
)
from tap_checkly.api.common.raw.auth import (
    Credentials,
)
from typing import (
    Any,
    Callable,
    List,
    NamedTuple,
)

API_URL_BASE = "https://api.checklyhq.com"
LOG = logging.getLogger(__name__)


def _get(creds: Credentials, endpoint: str, **kwargs: Any) -> List[JsonObj]:
    response = requests.get(
        f"{API_URL_BASE}{endpoint}",
        headers={"Authorization": f"Bearer {creds.api_key}"},
        **kwargs,
    )
    response.raise_for_status()
    LOG.debug("API call: %s\nkwargs = %s", endpoint, kwargs)
    return JsonFactory.build_json_list(response.json())


class Client(NamedTuple):
    get: Callable[..., List[JsonObj]]

    @classmethod
    def new(cls, creds: Credentials) -> Client:
        return cls(get=partial(_get, creds))
