from __future__ import (
    annotations,
)

import logging
from paginator.int_index.objs import (
    PageId,
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
    Optional,
)
from utils_logger import (
    DEBUG,
)

LOG = logging.getLogger(__name__)
API_URL_BASE = "https://gitlab.com/api/v4"


class RawClient(NamedTuple):
    creds: Credentials

    def get(
        self,
        endpoint: str,
        params: Dict[str, Any],
        page: Optional[PageId] = None,
    ) -> IO[Response]:
        _params = params.copy()
        if page:
            if _params.get("page") or _params.get("per_page"):
                LOG.warning("Overwriting params `page` and/or `per_page`")
            _params["page"] = page.page
            _params["per_page"] = page.per_page
        LOG.debug("GET\n\tendpoint: %s\n\tparams: %s", endpoint, _params)
        response = requests.get(
            "".join([API_URL_BASE, endpoint]),
            headers={"Private-Token": self.creds.api_key},
            params=_params,
        )
        LOG.debug(response)
        response.raise_for_status()
        if DEBUG and not response.json():
            LOG.debug("Empty json response")
        return IO(response)
