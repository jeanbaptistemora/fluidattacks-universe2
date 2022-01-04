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
    from_reg,
    from_stamp,
    RawRow,
    to_dict,
)
from code_etl.objs import (
    CommitStamp,
    RepoContex,
    RepoId,
    RepoRegistration,
)
from code_etl.utils import (
    COMMIT_HASH_SENTINEL,
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
import psycopg2
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
from returns.converters import (
    result_to_maybe,
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
from typing import (
    Type,
    TypeVar,
)

LOG = logging.getLogger(__name__)
_T = TypeVar("_T")


def all_data_count(client: Client, table: TableID) -> IO[ResultE[int]]:
    return client.cursor.execute_query(query.all_data_count(table)).bind(
        lambda _: client.cursor.fetch_one().map(
            lambda i: assert_key(i, 0).bind(lambda j: assert_type(j, int))
        )
    )


def _fetch(
    client: Client, chunk: int
) -> IO[Maybe[FrozenList[ResultE[CommitTableRow]]]]:
    try:
        return client.cursor.fetch_many(chunk).map(
            lambda rows: Maybe.from_optional(
                tuple(from_raw(RawRow(*r)) for r in rows) if rows else None
            )
        )
    except psycopg2.ProgrammingError:
        return IO(Maybe.empty)


def _all_data(
    client: Client, table: TableID, namespace: Maybe[str]
) -> PureIter[IO[ResultE[CommitTableRow]]]:
    pkg_items = 2000
    statement = namespace.map(
        lambda n: query.namespace_data(table, n)
    ).or_else_call(lambda: query.all_data(table))
    client.cursor.execute_query(statement)
    items = infinite_range(0, 1).map(lambda _: _fetch(client, pkg_items))
    return chain(until_empty(items).map(lambda i: i.map(from_flist)))


def namespace_data(
    client: Client, table: TableID, namespace: str
) -> PureIter[IO[ResultE[CommitTableRow]]]:
    return _all_data(client, table, Maybe.from_value(namespace))


def all_data_raw(
    client: Client, table: TableID
) -> PureIter[IO[ResultE[CommitTableRow]]]:
    return _all_data(client, table, Maybe.empty)


def insert_rows(
    client: Client, table: TableID, rows: FrozenList[CommitTableRow]
) -> IO[None]:
    LOG.debug("inserting %s rows", len(rows))
    return client.cursor.execute_batch(
        query.insert_row(table), [SqlArgs(to_dict(r)) for r in rows]
    )


def insert_unique_rows(
    client: Client, table: TableID, rows: FrozenList[CommitTableRow]
) -> IO[None]:
    LOG.debug("unique inserting %s rows", len(rows))
    return client.cursor.execute_batch(
        query.insert_unique_row(table), [SqlArgs(to_dict(r)) for r in rows]
    )


def _fetch_one(client: Client, d_type: Type[_T]) -> IO[ResultE[_T]]:
    return (
        client.cursor.fetch_one()
        .map(lambda l: assert_key(l, 0))
        .map(lambda v: v.bind(lambda i: assert_type(i, d_type)))
    )


def _fetch_not_empty(client: Client) -> IO[bool]:
    return client.cursor.fetch_one().map(lambda i: bool(i))


def get_context(
    client: Client, table: TableID, repo: RepoId
) -> IO[RepoContex]:
    last = client.cursor.execute_query(
        query.last_commit_hash(table, repo)
    ).bind(lambda _: _fetch_one(client, str))
    is_new = (
        client.cursor.execute_query(
            query.commit_exists(table, repo, COMMIT_HASH_SENTINEL),
        )
        .bind(lambda _: _fetch_not_empty(client))
        .map(lambda b: not b)
    )
    return last.bind(
        lambda l: is_new.map(lambda n: RepoContex(repo, result_to_maybe(l), n))
    )


def register_repos(
    client: Client, table: TableID, reg: FrozenList[RepoRegistration]
) -> IO[None]:
    LOG.info("register_repos %s", str(reg))
    encoded = tuple(from_reg(r) for r in reg)
    return insert_unique_rows(client, table, encoded)


def insert_stamps(
    client: Client, table: TableID, stamps: FrozenList[CommitStamp]
) -> IO[None]:
    LOG.info("inseting %s stamps", len(stamps))
    encoded = tuple(from_stamp(s) for s in stamps)
    return insert_unique_rows(client, table, encoded)


def _delta_fields(old: CommitTableRow, new: CommitTableRow) -> FrozenList[str]:
    _filter = filter(
        lambda x: x[0],
        ((bool(getattr(new, k) != v), k) for k, v in old.__dict__.items()),
    )
    return tuple(map(lambda x: x[1], _filter))


def delta_update(
    client: Client, table: TableID, old: CommitTableRow, new: CommitTableRow
) -> IO[None]:
    _fields = _delta_fields(old, new)
    if len(_fields) > 0:
        LOG.info("delta update %s fields", len(_fields))
        return client.cursor.execute_query(
            query.update_row(table, new, _fields)
        )
    LOG.info("delta update skipped")
    return IO(None)
