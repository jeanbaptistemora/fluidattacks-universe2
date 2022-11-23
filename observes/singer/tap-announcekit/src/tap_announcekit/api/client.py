from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
import logging
from purity.v1 import (
    Patch,
    Transform,
)
from returns.io import (
    IO,
)
from returns.primitives.hkt import (
    SupportsKind1,
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
    TypeVar,
)

API_ENDPOINT = "https://announcekit.app/gq/v2"
LOG = logging.getLogger(__name__)
_T = TypeVar("_T")


class Operation(GQL_Operation):
    # pylint: disable=too-few-public-methods
    # wrapper for making unfollowed import sgqlc.operation.Operation
    # not equivalent to Any type
    pass


@dataclass(frozen=True)
class _Query(SupportsKind1["_Query[_T]", _T]):
    # Instances of this class are NOT type safe
    # therefore it must be tested
    _raw_op: Patch[Callable[[], Operation]]
    from_raw: Transform[Any, _T]


class Query(_Query[_T]):
    def __init__(self, obj: _Query[_T]) -> None:
        super().__init__(obj._raw_op, obj.from_raw)

    def operation(self) -> Operation:
        return self._raw_op.unwrap()

    def __str__(self) -> str:
        return str(self.operation())


@dataclass(frozen=True)
class QueryFactory:
    @staticmethod
    def _new_op() -> Operation:
        return Operation(gql_schema.Query)

    @staticmethod
    def select(
        selections: Callable[[Operation], IO[None]],
        from_raw: Transform[Any, _T],
    ) -> Query[_T]:
        def op_obj() -> Operation:
            obj = QueryFactory._new_op()
            selections(obj)  # call equivalent to unsafe_perform_io
            return obj

        draft = _Query(Patch(op_obj), from_raw)
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

    @staticmethod
    def from_data(query: Query[_T], raw_data: Any) -> _T:
        gql_op = query.operation()
        return query.from_raw(gql_op + raw_data)

    def get(self, query: Query[_T]) -> IO[_T]:
        LOG.debug("Api call: %s", query)
        data = self._endpoint(query.operation())
        return IO(self.from_data(query, data))
