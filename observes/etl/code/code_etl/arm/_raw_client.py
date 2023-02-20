from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    JsonObj,
    JsonValue,
)
from fa_purity.frozen import (
    FrozenDict,
)
from fa_purity.json.factory import (
    from_any,
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
)

API_ENDPOINT = "https://app.fluidattacks.com/api"


@dataclass(frozen=True)
class ApiError(Exception):
    errors: JsonValue

    def to_exception(self) -> Exception:
        return Exception(self)


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

    def get(self, query: str, values: FrozenDict[str, str]) -> Cmd[JsonObj]:
        def _action() -> JsonObj:
            return from_any(
                self._inner.client.execute(gql(query), dict(values))  # type: ignore[misc]
            ).unwrap()

        return Cmd.from_cmd(_action)
