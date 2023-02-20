from __future__ import (
    annotations,
)

from ._retry import (
    delay,
    handlers,
    retry_cmd,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    JsonObj,
    JsonValue,
    ResultE,
)
from fa_purity.frozen import (
    FrozenDict,
)
from fa_purity.json.factory import (
    from_any,
)
from fa_purity.utils import (
    raise_exception,
)
from gql import (
    Client,
    gql,
)
from gql.transport.requests import (
    RequestsHTTPTransport,
)
from typing import (
    Dict,
    TypeVar,
)

API_ENDPOINT = "https://app.fluidattacks.com/api"
_T = TypeVar("_T")


@dataclass(frozen=True)
class ApiError(Exception):
    errors: JsonValue

    def to_exception(self) -> Exception:
        return Exception(self)


def error_handler(cmd: Cmd[_T]) -> Cmd[ResultE[_T]]:
    return handlers.too_many_requests_handler(
        handlers.server_error_handler(cmd)
    ).map(lambda r: r.bind(lambda x: x))


@dataclass(frozen=True)
class _GraphQlAsmClient:
    client: Client


@dataclass(frozen=True)
class GraphQlAsmClient:
    _inner: _GraphQlAsmClient

    @staticmethod
    def new(token: str) -> Cmd[GraphQlAsmClient]:
        def _new() -> GraphQlAsmClient:
            headers: Dict[str, str] = {"Authorization": f"Bearer {token}"}
            transport = RequestsHTTPTransport(API_ENDPOINT, headers)
            client = Client(
                transport=transport, fetch_schema_from_transport=True
            )
            return GraphQlAsmClient(_GraphQlAsmClient(client))

        return Cmd.from_cmd(_new)

    def _get(self, query: str, values: FrozenDict[str, str]) -> Cmd[JsonObj]:
        def _action() -> JsonObj:
            return from_any(
                self._inner.client.execute(gql(query), dict(values))  # type: ignore[misc]
            ).unwrap()

        return Cmd.from_cmd(_action)

    def get(self, query: str, values: FrozenDict[str, str]) -> Cmd[JsonObj]:
        return retry_cmd(
            error_handler(self._get(query, values)),
            lambda i, r: delay.delay_if_fail(i, r, i**2),
            10,
        ).map(lambda x: x.alt(raise_exception).unwrap())
