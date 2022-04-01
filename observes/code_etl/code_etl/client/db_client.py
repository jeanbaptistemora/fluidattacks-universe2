from dataclasses import (
    dataclass,
)
from fa_purity.cmd import (
    Cmd,
)
from fa_purity.frozen import (
    FrozenList,
)
import logging
from postgres_client.client import (
    Client,
)
from postgres_client.query import (
    Query,
    SqlArgs,
)
from returns.io import (
    IO,
)
from returns.unsafe import (
    unsafe_perform_io,
)
from typing import (
    Any,
    Callable,
    TypeVar,
)

LOG = logging.getLogger(__name__)
_T = TypeVar("_T")


def _to_cmd(action: Callable[[], IO[_T]]) -> Cmd[_T]:
    return Cmd.from_cmd(lambda: unsafe_perform_io(action()))


@dataclass(frozen=True)
class DbClient:
    # db client wrapper for Cmd transform
    _client: Client

    def execute_query(self, _query: Query) -> Cmd[None]:
        return _to_cmd(lambda: self._client.cursor.execute_query(_query))

    def execute_batch(
        self, _query: Query, args: FrozenList[SqlArgs]
    ) -> Cmd[None]:
        return _to_cmd(
            lambda: self._client.cursor.execute_batch(_query, list(args))
        )

    def fetch_one(self) -> Cmd[FrozenList[Any]]:
        return _to_cmd(self._client.cursor.fetch_one)

    def fetch_many(self, chunk: int) -> Cmd[FrozenList[FrozenList[Any]]]:
        return _to_cmd(lambda: self._client.cursor.fetch_many(chunk))
