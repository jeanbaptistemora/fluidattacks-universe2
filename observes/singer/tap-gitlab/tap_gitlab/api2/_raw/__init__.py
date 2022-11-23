from __future__ import (
    annotations,
)

from . import (
    _retry,
)
from ._http import (
    HttpClient,
    UnexpectedServerResponse,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    FrozenDict,
    FrozenList,
    JsonObj,
    JsonValue,
    Result,
)
from fa_purity.utils import (
    raise_exception,
)
import logging
from requests.exceptions import (
    HTTPError,
)
from typing import (
    NoReturn,
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
    _creds: Credentials
    _client: HttpClient
    _max_retries: int

    @staticmethod
    def new(creds: Credentials) -> RawClient:
        return RawClient(
            creds,
            HttpClient("https://gitlab.com/api/v4"),
            150,
        )

    @staticmethod
    def _handler(
        item: Result[
            JsonObj | FrozenList[JsonObj], HTTPError | UnexpectedServerResponse
        ],
    ) -> Result[JsonObj | FrozenList[JsonObj], HTTPError]:
        def _handled_errors(
            error: HTTPError | UnexpectedServerResponse,
        ) -> HTTPError | NoReturn:
            if isinstance(error, UnexpectedServerResponse):
                raise error
            err_code: int = error.response.status_code  # type: ignore[misc]
            if err_code in (500, 502):
                return error
            raise error

        return item.alt(_handled_errors)

    @property
    def _headers(self) -> JsonObj:
        return FrozenDict({"Private-Token": JsonValue(self._creds.api_key)})

    def get(
        self, endpoint: str, params: JsonObj
    ) -> Cmd[JsonObj | FrozenList[JsonObj]]:
        handled = self._client.get(endpoint, self._headers, params).map(
            self._handler
        )
        return _retry.retry_cmd(
            handled,
            lambda i, r: _retry.delay_if_fail(i, r, i ^ 2),
            self._max_retries,
        ).map(lambda r: r.alt(raise_exception).unwrap())

    def get_list(
        self, endpoint: str, params: JsonObj
    ) -> Cmd[FrozenList[JsonObj]]:
        def assert_flist(
            item: JsonObj | FrozenList[JsonObj],
        ) -> FrozenList[JsonObj]:
            if isinstance(item, tuple):
                return item
            raise TypeError("Expected a FrozenList")

        return self.get(endpoint, params).map(assert_flist)

    def get_item(self, endpoint: str, params: JsonObj) -> Cmd[JsonObj]:
        def assert_json(item: JsonObj | FrozenList[JsonObj]) -> JsonObj:
            if not isinstance(item, tuple):
                return item
            raise TypeError("Expected a FrozenList")

        return self.get(endpoint, params).map(assert_json)

    @staticmethod
    def post_handler(item: Result[None, HTTPError]) -> Result[None, HTTPError]:
        def _handled_errors(
            error: HTTPError,
        ) -> HTTPError | NoReturn:
            err_code: int = error.response.status_code  # type: ignore[misc]
            if err_code in (409, 500, 502):
                return error
            raise error

        return item.alt(_handled_errors)

    def post(self, endpoint: str) -> Cmd[None]:
        handled = self._client.post(endpoint, self._headers).map(
            lambda x: self.post_handler(x)
        )
        _max_retries: int = 10

        def _next(
            retry: int, result: Result[None, HTTPError]
        ) -> Cmd[Result[None, HTTPError]]:
            return _retry.delay_if_fail(retry, result, retry ^ 2)

        return _retry.retry_cmd(handled, _next, _max_retries).map(
            lambda r: r.alt(raise_exception).unwrap()
        )
