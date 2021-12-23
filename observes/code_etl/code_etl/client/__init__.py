# pylint: skip-file

from code_etl.client import (
    query,
)
from code_etl.client.decoder import (
    assert_int,
    assert_key,
    RawRow,
)
import logging
from postgres_client.client import (
    Client,
)
from postgres_client.ids import (
    TableID,
)
from purity.v1.pure_iter import (
    PureIter,
)
from purity.v1.pure_iter.factory import (
    from_flist,
    infinite_range,
)
from purity.v1.pure_iter.transform.io import (
    chain,
    until_empty,
)
from purity.v2.frozen import (
    FrozenList,
)
from returns.io import (
    IO,
)
from returns.maybe import (
    Maybe,
)
from returns.pointfree import (
    unify,
)
from returns.result import (
    Result,
)
from typing import (
    Union,
)

LOG = logging.getLogger(__name__)


def all_data_count(
    client: Client, table: TableID
) -> IO[Result[int, Union[KeyError, TypeError]]]:
    return client.cursor.execute_query(query.all_data_count(table)).bind(
        lambda _: client.cursor.fetch_one().map(
            lambda i: unify(assert_int)(assert_key(i, 0))
        )
    )


def _fetch(client: Client, chunk: int) -> IO[Maybe[FrozenList[RawRow]]]:
    return client.cursor.fetch_many(chunk).map(
        lambda rows: Maybe.from_optional(
            tuple(RawRow(*r) for r in rows) if rows else None
        )
    )


def all_data_raw(client: Client, table: TableID) -> PureIter[IO[RawRow]]:
    pkg_items = 2000
    client.cursor.execute_query(query.all_data(table))
    items = infinite_range(0, 1).map(lambda _: _fetch(client, pkg_items))
    return chain(until_empty(items).map(lambda i: i.map(from_flist)))
