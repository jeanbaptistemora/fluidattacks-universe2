# pylint: skip-file

from code_etl.client import (
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
    gen_fa_hash,
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
)
from postgres_client.ids import (
    TableID,
)
from purity.v1 import (
    Flattener,
)
from purity.v1.pure_iter.transform.io import (
    consume,
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
    Union,
)

LOG = logging.getLogger(__name__)


def migrate_commit(
    raw: CommitTableRow,
) -> ResultE[CommitStamp]:
    data = decode_commit_data_2(raw)
    _id = data.map(
        lambda cd: CommitDataId(
            raw.namespace,
            raw.repository,
            CommitId(raw.hash, gen_fa_hash(cd)),
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


def migration(
    client: Client,
    client_2: Client,
    table: TableID,
) -> IO[ResultE[None]]:
    data = (
        all_data_raw(client, table)
        .map(lambda i: i.map(lambda r: r.bind(migrate_row)))
        .chunked(100)
        .map(
            lambda i: Flattener.list_io(tuple(i)).map(
                lambda l: Flattener.result_list(l)
            )
        )
    )
    result = data.map(
        lambda i: i.map(
            lambda r: r.map(lambda t: tuple(from_row_obj(j) for j in t)).map(
                lambda n: insert_rows(client_2, table, n)
            )
        )
    )
    try:
        return consume(result.map(lambda a: a.bind(lambda d: d.unwrap()))).map(
            Success
        )
    except UnwrapFailedError as err:
        return IO(Failure(err.halted_container.failure()))
