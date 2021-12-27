# pylint: skip-file

from code_etl.client import (
    all_data_count,
    all_data_raw,
    insert_rows,
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
from code_etl.objs import (
    Commit,
    CommitDataId,
    CommitId,
    CommitStamp,
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
from returns.io import (
    IO,
)
from returns.primitives.exceptions import (
    UnwrapFailedError,
)
from returns.result import (
    Failure,
    ResultE,
    Success,
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
            raw.namespace,
            raw.repository,
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
    ] = decode_repo_registration(row)
    return reg.lash(lambda _: migrate_commit(row))


def _progress(count: int, total: int) -> IO[None]:
    LOG.info("Migration %s/%s [%s%%]", count, total, (count * 100) // total)
    return IO(None)


def migration(
    client: Client,
    client_2: Client,
    source: TableID,
    target: TableID,
) -> IO[ResultE[None]]:
    data = (
        all_data_raw(client, source)
        .map(lambda i: i.map(lambda r: r.bind(migrate_row)))
        .chunked(100)
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
        count = IO(0)
        total = all_data_count(client, source).map(lambda i: i.unwrap())
        total.bind(lambda t: _log_info("Total rows: %s", t))
        for items in data:
            _items = items.map(lambda i: i.unwrap())
            pkg_len = _items.map(lambda i: len(i))
            count = count.bind(lambda c: pkg_len.map(lambda l: c + l))
            _items.bind(lambda i: insert_rows(client_2, target, i)).bind(
                lambda _: count.bind(
                    lambda c: total.map(lambda t: _progress(c, t))
                )
            )
        return IO(Success(None))
    except UnwrapFailedError as err:
        return IO(Failure(err.halted_container.failure()))


def start(
    db_id: DatabaseID,
    creds: Credentials,
    source: TableID,
    target: TableID,
) -> IO[None]:
    client = ClientFactory().from_creds(db_id, creds)
    client2 = ClientFactory().from_creds(db_id, creds)
    return migration(client, client2, source, target).map(lambda i: i.unwrap())
