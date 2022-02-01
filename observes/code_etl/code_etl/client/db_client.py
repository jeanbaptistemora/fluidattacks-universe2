from dataclasses import (
    dataclass,
)
import logging
from postgres_client.client import (
    Client,
)
from postgres_client.query import (
    Query,
    SqlArgs,
)
from purity.adapters.to_v2 import (
    to_cmd,
)
from purity.v2.cmd import (
    Cmd,
)
from purity.v2.frozen import (
    FrozenList,
)
from typing import (
    Any,
)

LOG = logging.getLogger(__name__)


@dataclass(frozen=True)
class DbClient:
    # db client wrapper for Cmd transform
    _client: Client

    def execute_query(self, _query: Query) -> Cmd[None]:
        return to_cmd(lambda: self._client.cursor.execute_query(_query))

    def execute_batch(
        self, _query: Query, args: FrozenList[SqlArgs]
    ) -> Cmd[None]:
        return to_cmd(
            lambda: self._client.cursor.execute_batch(_query, list(args))
        )

    def fetch_one(self) -> Cmd[FrozenList[Any]]:
        return to_cmd(self._client.cursor.fetch_one)

    def fetch_many(self, chunk: int) -> Cmd[FrozenList[FrozenList[Any]]]:
        return to_cmd(lambda: self._client.cursor.fetch_many(chunk))
