from code_etl.client import (
    all_data_count,
    insert_rows,
    namespace_data,
)
from code_etl.client.db_client import (
    DbClient,
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
from fa_purity.cmd import (
    Cmd,
    unsafe_unwrap,
)
from fa_purity.flatten import (
    flatten_results,
)
from fa_purity.frozen import (
    FrozenList,
)
from fa_purity.result import (
    ResultE,
)
from fa_purity.stream.transform import (
    consume,
)
from fa_purity.union import (
    inl,
)
import logging
from postgres_client.client import (
    ClientFactory,
)
from postgres_client.connection import (
    Credentials,
    DatabaseID,
)
from postgres_client.ids import (
    TableID,
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
            RepoId(raw.namespace, raw.repository),
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
    ] = decode_repo_registration(row).map(inl)
    return reg.lash(lambda _: migrate_commit(row).map(inl))


def migration(
    client: DbClient,
    client_2: DbClient,
    source: TableID,
    target: TableID,
    namespace: str,
) -> Cmd[None]:
    # pylint: disable=unnecessary-lambda
    adjusted_data = namespace_data(client, source, namespace).map(
        lambda s: s.map(lambda r: r.bind(migrate_row)).chunked(2000)
    )
    counter = [0]
    total = all_data_count(client_2, source, namespace).map(
        lambda i: i.unwrap()
    )

    def _emit_action(
        client: DbClient,
        target: TableID,
        total_items: int,
        pkg: FrozenList[CommitTableRow],
    ) -> None:
        pkg_len = len(pkg)
        unsafe_unwrap(insert_rows(client, target, pkg))
        counter[0] = counter[0] + pkg_len
        LOG.info(
            "Migration %s/%s [%s%%]",
            counter[0],
            total_items,
            (counter[0] * 100) // total_items,
        )

    action = total.bind(
        lambda t: Cmd.from_cmd(lambda: LOG.info("Total rows: %s", t)).bind(
            lambda _: adjusted_data.map(
                lambda s: s.map(lambda i: flatten_results(i))
                .map(
                    lambda r: r.map(
                        lambda l: tuple(from_row_obj(i) for i in l)
                    ).map(
                        lambda p: Cmd.from_cmd(
                            lambda: _emit_action(client_2, target, t, p)
                        )
                    )
                )
                .map(lambda x: x.unwrap())
            )
        )
    )
    return action.bind(consume)


def start(
    db_id: DatabaseID,
    creds: Credentials,
    source: TableID,
    target: TableID,
    namespace: str,
) -> Cmd[None]:
    client = DbClient(ClientFactory().from_creds(db_id, creds))
    client2 = DbClient(ClientFactory().from_creds(db_id, creds))
    return init_table_2_query(client, target).bind(
        lambda _: migration(client, client2, source, target, namespace)
    )
