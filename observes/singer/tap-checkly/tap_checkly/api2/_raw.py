from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    JsonObj,
)
from fa_purity.json.factory import (
    from_any,
)
from fa_purity.json.transform import (
    to_raw,
)
import logging
import requests  # type: ignore[import]

LOG = logging.getLogger(__name__)


@dataclass(frozen=True)
class Credentials:
    account: str
    api_key: str

    def __str__(self) -> str:
        return "masked api_key"


@dataclass(frozen=True)
class RawClient:
    _auth: Credentials
    _api_url: str = "https://api.checklyhq.com"

    def _full_endpoint(self, endpoint: str) -> str:
        return self._api_url + endpoint

    def get(self, endpoint: str, params: JsonObj) -> Cmd[JsonObj]:
        def _action() -> JsonObj:
            target = self._full_endpoint(endpoint)
            LOG.debug("API call: %s\nparams = %s", target, params)
            response = requests.get(  # type: ignore[misc]
                target,
                headers={
                    "X-Checkly-Account": self._auth.account,
                    "Authorization": f"Bearer {self._auth.api_key}",
                },
                params=to_raw(params),  # type: ignore[misc]
            )
            response.raise_for_status()  # type: ignore[misc]
            return from_any(response.json()).unwrap()  # type: ignore[misc]

        return Cmd.from_cmd(_action)
