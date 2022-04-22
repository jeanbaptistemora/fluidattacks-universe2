from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    FrozenList,
    JsonObj,
    Maybe,
    Result,
)
from fa_purity.json.factory import (
    from_any,
    json_list,
)
from fa_purity.json.transform import (
    to_raw,
)
from fa_purity.union import (
    UnionFactory,
)
from fa_purity.utils import (
    raise_exception,
)
import logging
import requests

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

    def get(
        self, endpoint: str, params: JsonObj
    ) -> Cmd[JsonObj | FrozenList[JsonObj]]:
        def _action() -> FrozenList[JsonObj] | JsonObj:
            target = self._full_endpoint(endpoint)
            LOG.debug("API call: %s\nparams = %s", target, params)
            response = requests.get(
                target,
                headers={  # type: ignore[misc]
                    "X-Checkly-Account": self._auth.account,
                    "Authorization": f"Bearer {self._auth.api_key}",
                },
                params=to_raw(params),  # type: ignore[misc]
            )
            _union: UnionFactory[JsonObj, FrozenList[JsonObj]] = UnionFactory()
            response.raise_for_status()
            raw = response.json()  # type: ignore[misc]
            result = json_list(raw).map(_union.inr).lash(lambda _: from_any(raw).map(_union.inl))  # type: ignore[misc]
            return result.unwrap()

        return Cmd.from_cmd(_action)

    def get_list(
        self, endpoint: str, params: JsonObj
    ) -> Cmd[FrozenList[JsonObj]]:
        return (
            self.get(endpoint, params)
            .map(
                lambda x: Maybe.from_optional(
                    x if isinstance(x, tuple) else None
                )
                .to_result()
                .alt(
                    lambda _: Exception(f"Expected a FrozenList got {type(x)}")
                )
            )
            .map(lambda r: r.alt(raise_exception).unwrap())
        )

    def get_item(self, endpoint: str, params: JsonObj) -> Cmd[JsonObj]:
        return (
            self.get(endpoint, params)
            .map(
                lambda x: Maybe.from_optional(
                    x if not isinstance(x, tuple) else None
                )
                .to_result()
                .alt(lambda _: Exception(f"Expected a JsonObj got {type(x)}"))
            )
            .map(lambda r: r.alt(raise_exception).unwrap())
        )
