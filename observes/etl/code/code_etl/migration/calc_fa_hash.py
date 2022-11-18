# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from code_etl.client._raw import (
    RawClient,
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
from redshift_client.id_objs import (
    TableId,
)
from redshift_client.sql_client import (
    new_client,
)
from redshift_client.sql_client.connection import (
    connect,
    Credentials,
    DatabaseId,
    DbConnection,
    IsolationLvl,
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
    ] = decode_repo_registration(row).map(lambda x: inl(x))
    return reg.lash(lambda _: migrate_commit(row).map(lambda x: inl(x)))


def migration(
    source_client: RawClient,
    source_client_2: RawClient,
    target_client: RawClient,
    namespace: str,
) -> Cmd[None]:
    adjusted_data = source_client.namespace_data(namespace).map(
        lambda s: s.map(lambda r: r.bind(migrate_row)).chunked(2000)
    )
    counter = [0]
    total = source_client_2.all_data_count(namespace).map(lambda i: i.unwrap())

    def _emit_action(
        total_items: int,
        pkg: FrozenList[CommitTableRow],
    ) -> None:
        pkg_len = len(pkg)
        unsafe_unwrap(target_client.insert_rows(pkg))
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
                        lambda d: tuple(from_row_obj(i) for i in d)
                    ).map(lambda p: Cmd.from_cmd(lambda: _emit_action(t, p)))
                )
                .map(lambda x: x.unwrap())
            )
        )
    )
    return action.bind(consume)


def _start(
    connection: DbConnection,
    source: TableId,
    target: TableId,
    namespace: str,
) -> Cmd[None]:
    sql_client_1 = new_client(connection, LOG.getChild("sql_client_1"))
    sql_client_2 = new_client(connection, LOG.getChild("sql_client_2"))
    sql_client_3 = new_client(connection, LOG.getChild("sql_client_3"))
    sql_client_target = new_client(
        connection, LOG.getChild("sql_client_target")
    )

    client = sql_client_1.map(lambda q: RawClient(q, source))
    client2 = sql_client_2.map(lambda q: RawClient(q, source))
    target_client = sql_client_target.map(lambda q: RawClient(q, target))
    return sql_client_3.bind(
        lambda c3: client.bind(
            lambda c1: client2.bind(
                lambda c2: target_client.bind(
                    lambda ct: init_table_2_query(c3, target).bind(
                        lambda _: migration(c1, c2, ct, namespace)
                    )
                )
            )
        )
    )


def start(
    db_id: DatabaseId,
    creds: Credentials,
    source: TableId,
    target: TableId,
    namespace: str,
) -> Cmd[None]:
    connection = connect(
        db_id,
        creds,
        False,
        IsolationLvl.AUTOCOMMIT,
    )

    def _action() -> None:
        conn = unsafe_unwrap(connection)
        try:
            unsafe_unwrap(_start(conn, source, target, namespace))
        finally:
            unsafe_unwrap(conn.close())

    return Cmd.from_cmd(_action)
