# pylint: skip-file

from code_etl.client import (
    query,
)
from code_etl.client._assert import (
    assert_key,
    assert_type,
)
from code_etl.client.encoder import (
    CommitTableRow,
    from_raw,
    RawRow,
    to_dict,
)
import logging
from postgres_client.client import (
    Client,
)
from postgres_client.ids import (
    TableID,
)
from postgres_client.query import (
    SqlArgs,
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
from returns.result import (
    ResultE,
)

LOG = logging.getLogger(__name__)


def all_data_count(client: Client, table: TableID) -> IO[ResultE[int]]:
    return client.cursor.execute_query(query.all_data_count(table)).bind(
        lambda _: client.cursor.fetch_one().map(
            lambda i: assert_key(i, 0).bind(lambda j: assert_type(j, int))
        )
    )


def _fetch(
    client: Client, chunk: int
) -> IO[Maybe[FrozenList[ResultE[CommitTableRow]]]]:
    return client.cursor.fetch_many(chunk).map(
        lambda rows: Maybe.from_optional(
            tuple(from_raw(RawRow(*r)) for r in rows) if rows else None
        )
    )


def all_data_raw(
    client: Client, table: TableID
) -> PureIter[IO[ResultE[CommitTableRow]]]:
    pkg_items = 2000
    client.cursor.execute_query(query.all_data(table))
    items = infinite_range(0, 1).map(lambda _: _fetch(client, pkg_items))
    return chain(until_empty(items).map(lambda i: i.map(from_flist)))


def insert_rows(
    client: Client, table: TableID, rows: FrozenList[CommitTableRow]
) -> IO[None]:
    return client.cursor.execute_batch(
        query.insert_row(table), [SqlArgs(to_dict(r)) for r in rows]
    )
