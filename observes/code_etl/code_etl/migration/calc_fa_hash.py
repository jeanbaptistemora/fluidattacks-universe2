from code_etl.client import (
    all_data_count,
    insert_rows,
    namespace_data,
)
from code_etl.client.decoder import (
    decode_commit_data_2,
    decode_repo_registration,
)
from code_etl.client.encoder import (
    CommitTableRow,
    from_row_obj,
)
from code_etl.factories import (
    gen_fa_hash_2,
)
from code_etl.migration.tables import (
    init_table_2_query,
)
from code_etl.objs import (
    Commit,
    CommitDataId,
    CommitId,
    CommitStamp,
    RepoId,
    RepoRegistration,
)
import logging
from postgres_client.client import (
    Client,
    ClientFactory,
)
from postgres_client.connection import (
    Credentials,
    DatabaseID,
)
from postgres_client.ids import (
    TableID,
)
from purity.v1 import (
    Flattener,
)
from purity.v2.adapters import (
    from_returns,
    to_returns,
)
from purity.v2.frozen import (
    FrozenList,
)
from purity.v2.pure_iter.transform.io import (
    consume,
)
from purity.v2.result import (
    Result,
    ResultE,
    UnwrapError,
)
from purity.v2.union import (
    inl,
)
from returns.io import (
    IO,
)
from typing import (
    Any,
    Union,
)

LOG = logging.getLogger(__name__)


def _log_info(msg: str, *args: Any) -> IO[None]:
    LOG.info(msg, *args)
    return IO(None)


def migrate_commit(
    raw: CommitTableRow,
) -> ResultE[CommitStamp]:
    data = decode_commit_data_2(raw)
    _id = data.map(
        lambda cd: CommitDataId(
            RepoId(raw.namespace, raw.repository),
            CommitId(raw.hash, gen_fa_hash_2(cd)),
        )
    )
    commit = data.bind(lambda d: _id.map(lambda i: Commit(i, d)))
    return commit.map(lambda c: CommitStamp(c, raw.seen_at))


def migrate_row(
    row: CommitTableRow,
) -> ResultE[Union[CommitStamp, RepoRegistration]]:
    reg: ResultE[
        Union[CommitStamp, RepoRegistration]
    ] = decode_repo_registration(row).map(inl)
    return reg.lash(lambda _: migrate_commit(row).map(inl))


def _progress(count: int, total: int) -> IO[None]:
    LOG.info("Migration %s/%s [%s%%]", count, total, (count * 100) // total)
    return IO(None)


def migration(
    client: Client,
    client_2: Client,
    source: TableID,
    target: TableID,
    namespace: str,
) -> IO[ResultE[None]]:
    # pylint: disable=unnecessary-lambda
    data = (
        namespace_data(client, source, namespace)
        .map(
            lambda i: i.map(
                lambda r: r.bind(lambda x: to_returns(migrate_row(x)))
            )
        )
        .chunked(2000)
        .map(
            lambda i: Flattener.list_io(tuple(i)).map(
                lambda l: Flattener.result_list(l)
            )
        )
        .map(
            lambda i: i.map(
                lambda r: r.map(lambda t: tuple(from_row_obj(j) for j in t))
            )
        )
    )
    try:
        counter = IO(0)
        total = all_data_count(client_2, source).map(lambda i: i.unwrap())
        total.bind(lambda t: _log_info("Total rows: %s", t))

        def _emit(
            items: IO[Result[FrozenList[CommitTableRow], Exception]]
        ) -> IO[None]:
            _items = items.map(lambda i: i.unwrap())
            pkg_len = _items.map(lambda i: len(i))
            count = counter.bind(lambda c: pkg_len.map(lambda l: c + l))
            return _items.bind(
                lambda i: insert_rows(client_2, target, i)
            ).bind(
                lambda _: count.bind(
                    lambda c: total.bind(lambda t: _progress(c, t))
                )
            )

        consume(data.map(lambda x: _emit(x.map(from_returns))))
        return IO(Result.success(None))
    except UnwrapError[Any, Exception] as err:
        return IO(Result.failure(err.container.unwrap_fail()))


def start(
    db_id: DatabaseID,
    creds: Credentials,
    source: TableID,
    target: TableID,
    namespace: str,
) -> IO[None]:
    client = ClientFactory().from_creds(db_id, creds)
    client2 = ClientFactory().from_creds(db_id, creds)
    return init_table_2_query(client, target).bind(
        lambda _: migration(client, client2, source, target, namespace).map(
            lambda i: i.unwrap()
        )
    )
