from dataclasses import (
    dataclass,
)
from returns.io import (
    IO,
)
from returns.unsafe import (
    unsafe_perform_io,
)
from sgqlc import (
    introspection,
)
from sgqlc.endpoint.http import (
    HTTPEndpoint,
)
from sgqlc.operation import (
    Operation,
)
from tap_announcekit.api import (
    gql_schema,
)
from tap_announcekit.api.auth import (
    Creds,
)
from typing import (
    Any,
)

API_ENDPOINT = "https://announcekit.app/gq/v2"


@dataclass(frozen=True)
class _Query:
    raw: Operation  # equivalent to Any


class Query(_Query):
    # pylint: disable=too-few-public-methods
    def __init__(self, obj: _Query) -> None:
        for key, val in obj.__dict__.items():
            object.__setattr__(self, key, val)


@dataclass(frozen=True)
class _ApiClient:
    _endpoint: HTTPEndpoint


class ApiClient(_ApiClient):
    def __init__(self, creds: Creds) -> None:
        obj = _ApiClient(HTTPEndpoint(API_ENDPOINT, creds.basic_auth_header()))
        for key, val in obj.__dict__.items():
            object.__setattr__(self, key, val)

    @staticmethod
    def new_query() -> IO[Query]:
        draft = _Query(Operation(gql_schema.Query))
        return IO(Query(draft))

    def introspection_data(self) -> Any:
        return self._endpoint(
            introspection.query,
            introspection.variables(
                include_description=False,
                include_deprecated=False,
            ),
        )

    def get(self, query: IO[Query]) -> IO[Any]:
        raw_query = unsafe_perform_io(query).raw
        data = self._endpoint(raw_query)
        return IO(raw_query + data)
