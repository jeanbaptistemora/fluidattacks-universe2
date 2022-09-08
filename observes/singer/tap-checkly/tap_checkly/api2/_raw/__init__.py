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
    Result,
)
from fa_purity.json.errors.invalid_type import (
    InvalidType,
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
from requests.exceptions import (
    HTTPError,
)
from typing import (
    NoReturn,
    Union,
)

LOG = logging.getLogger(__name__)


@dataclass(frozen=True)
class Credentials:
    account: str
    api_key: str

    def __str__(self) -> str:
        return "masked api_key"


class UnexpectedServerResponse(Exception):
    pass


@dataclass(frozen=True)
class RawClient:
    _auth: Credentials
    _max_retries: int = 10
    _api_url: str = "https://api.checklyhq.com"

    def _full_endpoint(self, endpoint: str) -> str:
        return self._api_url + endpoint

    def _unhandled_get(
        self, endpoint: str, params: JsonObj
    ) -> Cmd[
        Result[
            JsonObj | FrozenList[JsonObj], HTTPError | UnexpectedServerResponse
        ]
    ]:
        def _action() -> Result[
            JsonObj | FrozenList[JsonObj], HTTPError | UnexpectedServerResponse
        ]:
            target = self._full_endpoint(endpoint)
            LOG.info("API call (get): %s\nparams = %s", target, params)
            response = requests.get(
                target,
                headers={  # type: ignore[misc]
                    "X-Checkly-Account": self._auth.account,
                    "Authorization": f"Bearer {self._auth.api_key}",
                },
                params=to_raw(params),  # type: ignore[misc]
            )
            _union: UnionFactory[JsonObj, FrozenList[JsonObj]] = UnionFactory()
            try:
                response.raise_for_status()
                raw = response.json()  # type: ignore[misc]
                result = json_list(raw).map(_union.inr).lash(lambda _: from_any(raw).map(_union.inl))  # type: ignore[misc]
                return result.alt(
                    lambda e: UnexpectedServerResponse(f"error: {str(e)}; raw response: {str(raw)}")  # type: ignore[misc]
                )
            except HTTPError as err:  # type: ignore[misc]
                return Result.failure(err)

        return Cmd.from_cmd(_action)

    def _handler(
        self,
        item: Result[
            JsonObj | FrozenList[JsonObj], HTTPError | UnexpectedServerResponse
        ],
    ) -> Result[JsonObj | FrozenList[JsonObj], HTTPError]:
        def _handled_errors(
            error: HTTPError | UnexpectedServerResponse,
        ) -> HTTPError | NoReturn:
            if isinstance(error, UnexpectedServerResponse):
                raise error
            if error.errno in (429,) or error.errno in range(500, 600):
                return error
            raise error

        return item.alt(_handled_errors)

    def get(
        self, endpoint: str, params: JsonObj
    ) -> Cmd[JsonObj | FrozenList[JsonObj]]:
        handled = self._unhandled_get(endpoint, params).map(self._handler)
        return _retry.retry_cmd(
            handled, self._max_retries, lambda i: i ^ 2
        ).map(lambda r: r.alt(raise_exception).unwrap())

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
