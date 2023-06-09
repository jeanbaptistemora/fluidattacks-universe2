from . import (
    _retry,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    FrozenDict,
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
from requests.exceptions import (
    HTTPError,
)
from typing import (
    NoReturn,
    TypeVar,
)

LOG = logging.getLogger(__name__)
_T = TypeVar("_T")


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

    def _raw_get(
        self, endpoint: str, params: JsonObj
    ) -> Cmd[
        Result[
            JsonObj | FrozenList[JsonObj], HTTPError | UnexpectedServerResponse
        ]
    ]:
        def _action() -> Result[
            JsonObj | FrozenList[JsonObj], HTTPError | UnexpectedServerResponse
        ]:
            union: UnionFactory[
                HTTPError, UnexpectedServerResponse
            ] = UnionFactory()
            target = self._full_endpoint(endpoint)
            LOG.info("API call (get): %s\nparams = %s", target, params)
            response = requests.get(
                target,
                headers={
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
                return Result.failure(union.inl(err))

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
            err_code: int = error.response.status_code  # type: ignore[misc]
            if err_code in (429,) or err_code in range(500, 600):
                return error
            raise error

        return item.alt(_handled_errors)

    def _server_error_handler(
        self, retry: int, result: Result[_T, HTTPError]
    ) -> Result[_T | None, HTTPError]:
        _union: UnionFactory[_T, None] = UnionFactory()

        def _handler(error: HTTPError) -> Result[_T | None, HTTPError]:
            err_code: int = error.response.status_code  # type: ignore[misc]
            threshold = round(self._max_retries * 0.4)
            if retry >= threshold and err_code in range(500, 600):
                return Result.success(None)
            return Result.failure(error)

        return result.map(_union.inl).lash(_handler)

    def get(
        self, endpoint: str, params: JsonObj
    ) -> Cmd[JsonObj | FrozenList[JsonObj] | None]:
        _union: UnionFactory[
            JsonObj | FrozenList[JsonObj], None
        ] = UnionFactory()
        handled = (
            self._raw_get(endpoint, params)
            .map(self._handler)
            .map(lambda r: r.map(_union.inl))
        )

        def _retry_cmd(
            retry: int,
            result: Result[JsonObj | FrozenList[JsonObj] | None, HTTPError],
        ) -> Cmd[Result[JsonObj | FrozenList[JsonObj] | None, HTTPError]]:
            retry_msg = Cmd.from_cmd(
                lambda: LOG.info("retry #%2s waiting...", retry)
            )
            delay = _retry.sleep_cmd(retry ^ 2)
            _delay = _retry.cmd_if_fail(result, retry_msg + delay)

            def _to_result(
                item: JsonObj | FrozenList[JsonObj] | None,
            ) -> Result[JsonObj | FrozenList[JsonObj] | None, HTTPError]:
                result: Result[
                    JsonObj | FrozenList[JsonObj] | None, HTTPError
                ] = Result.success(item)
                return result

            if endpoint.startswith("/v1/check-results"):
                return (
                    self._server_error_handler(retry, result)
                    .map(lambda x: Cmd.from_cmd(lambda: _to_result(x)))
                    .value_or(_delay)
                )
            return _delay

        return _retry.retry_cmd(
            handled, lambda i, r: _retry_cmd(i, r), self._max_retries
        ).map(lambda r: r.alt(raise_exception).unwrap())

    def get_list(
        self, endpoint: str, params: JsonObj
    ) -> Cmd[FrozenList[JsonObj]]:
        empty: FrozenList[JsonObj] = tuple()
        return (
            self.get(endpoint, params)
            .map(lambda x: empty if x is None else x)
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
        empty: JsonObj = FrozenDict({})
        return (
            self.get(endpoint, params)
            .map(lambda x: empty if x is None else x)
            .map(
                lambda x: Maybe.from_optional(
                    x if not isinstance(x, tuple) else None
                )
                .to_result()
                .alt(lambda _: Exception(f"Expected a JsonObj got {type(x)}"))
            )
            .map(lambda r: r.alt(raise_exception).unwrap())
        )
