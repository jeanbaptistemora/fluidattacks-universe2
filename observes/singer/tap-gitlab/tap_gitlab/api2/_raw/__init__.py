# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from . import (
    _retry,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    FrozenList,
    JsonObj,
    Maybe,
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
from typing import (
    TypeVar,
)

LOG = logging.getLogger(__name__)


@dataclass(frozen=True)
class Credentials:
    api_key: str

    def __repr__(self) -> str:
        return "Credentials([masked])"

    def __str__(self) -> str:
        return "Credentials([masked])"


_T = TypeVar("_T")


class UnexpectedType(Exception):
    def __init__(self, obj: _T, expected: str) -> None:
        super().__init__(
            f"Expected `{expected}` but got `{type(obj).__name__}`"
        )


@dataclass(frozen=True)
class RawClient:
    _auth: Credentials
    _max_retries: int = 150
    _api_url: str = "https://gitlab.com/api/v4"

    def _full_endpoint(self, endpoint: str) -> str:
        return self._api_url + endpoint

    def _unhandled_get(
        self, endpoint: str, params: JsonObj
    ) -> Cmd[JsonObj | FrozenList[JsonObj]]:
        def _action() -> FrozenList[JsonObj] | JsonObj:
            target = self._full_endpoint(endpoint)
            LOG.info("API call: %s\nparams = %s", target, params)
            response = requests.get(
                target,
                headers={
                    "Private-Token": self._auth.api_key,
                },
                params=to_raw(params),  # type: ignore[misc]
            )
            _union: UnionFactory[JsonObj, FrozenList[JsonObj]] = UnionFactory()
            response.raise_for_status()
            raw = response.json()  # type: ignore[misc]
            result = json_list(raw).map(_union.inr).lash(lambda _: from_any(raw).map(_union.inl))  # type: ignore[misc]
            return result.unwrap()

        return Cmd.from_cmd(_action)

    def get(
        self, endpoint: str, params: JsonObj
    ) -> Cmd[JsonObj | FrozenList[JsonObj]]:
        handled = _retry.api_handler(self._unhandled_get(endpoint, params))
        return _retry.retry_cmd(handled, self._max_retries, lambda i: i ^ 2)

    def get_list(
        self, endpoint: str, params: JsonObj
    ) -> Cmd[FrozenList[JsonObj]]:
        return self.get(endpoint, params).map(
            lambda x: Maybe.from_optional(x if isinstance(x, tuple) else None)
            .to_result()
            .alt(lambda _: UnexpectedType(x, "FrozenList"))
            .alt(raise_exception)
            .unwrap()
        )

    def get_item(self, endpoint: str, params: JsonObj) -> Cmd[JsonObj]:
        return self.get(endpoint, params).map(
            lambda x: Maybe.from_optional(
                x if not isinstance(x, tuple) else None
            )
            .to_result()
            .alt(lambda _: UnexpectedType(x, "JsonObj"))
            .alt(raise_exception)
            .unwrap()
        )
