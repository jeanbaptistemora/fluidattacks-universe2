from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
import logging
from purity.v1 import (
    Patch,
)
from returns.io import (
    IO,
)
from sgqlc import (
    introspection,
)
from sgqlc.endpoint.http import (
    HTTPEndpoint,
)
from sgqlc.operation import (
    Operation as GQL_Operation,
)
from tap_announcekit.api import (
    gql_schema,
)
from tap_announcekit.api.auth import (
    Creds,
)
from typing import (
    Any,
    Callable,
)

API_ENDPOINT = "https://announcekit.app/gq/v2"
LOG = logging.getLogger(__name__)


class Operation(GQL_Operation):
    # pylint: disable=too-few-public-methods
    # wrapper for making unfollowed import sgqlc.operation.Operation
    # not equivalent to Any type
    pass


@dataclass(frozen=True)
class _Query:
    _raw: Patch[Callable[[], Operation]]


class Query(_Query):
    def __init__(self, obj: _Query) -> None:
        super().__init__(obj._raw)

    def operation(self) -> Operation:
        return self._raw.unwrap()

    def __str__(self) -> str:
        return str(self.operation())


@dataclass(frozen=True)
class QueryFactory:
    @staticmethod
    def _new_op() -> Operation:
        return Operation(gql_schema.Query)

    @staticmethod
    def select(selections: Callable[[Operation], IO[None]]) -> Query:
        def op_obj() -> Operation:
            obj = QueryFactory._new_op()
            selections(obj)
            return obj

        draft = _Query(Patch(op_obj))
        return Query(draft)


@dataclass(frozen=True)
class _ApiClient:
    _endpoint: HTTPEndpoint


class ApiClient(_ApiClient):
    def __init__(self, creds: Creds) -> None:
        obj = _ApiClient(HTTPEndpoint(API_ENDPOINT, creds.basic_auth_header()))
        super().__init__(obj._endpoint)

    def introspection_data(self) -> Any:
        return self._endpoint(
            introspection.query,
            introspection.variables(
                include_description=False,
                include_deprecated=False,
            ),
        )

    def get(self, query: Query) -> IO[Any]:
        LOG.debug("Api call: %s", query)
        gql_op = query.operation()
        data = self._endpoint(gql_op)
        return IO(gql_op + data)
