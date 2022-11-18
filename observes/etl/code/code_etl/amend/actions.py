# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from code_etl.amend.core import (
    AmendUsers,
)
from code_etl.client import (
    Client,
)
from code_etl.mailmap import (
    Mailmap,
)
from code_etl.objs import (
    CommitStamp,
    RepoRegistration,
)
from fa_purity.cmd import (
    Cmd,
    unsafe_unwrap,
)
from fa_purity.maybe import (
    Maybe,
)
from fa_purity.stream.transform import (
    consume,
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


def _update(
    client: Client,
    mailmap: Maybe[Mailmap],
    item: Union[CommitStamp, RepoRegistration],
) -> Cmd[None]:
    if isinstance(item, CommitStamp):
        _item = item
        fixed = (
            mailmap.map(AmendUsers)
            .map(lambda a: a.amend_commit_stamp_users(_item))
            .value_or(_item)
        )
        return client.delta_update(item, fixed)
    return Cmd.from_cmd(lambda: None)


def amend_users(
    fetch_client: Client,
    update_client: Client,
    namespace: str,
    mailmap: Maybe[Mailmap],
) -> Cmd[None]:
    mutation_msg = Cmd.from_cmd(lambda: LOG.info("Mutation started"))
    data = fetch_client.namespace_data(namespace)
    result = data.bind(
        lambda s: s.map(lambda r: r.unwrap())
        .map(lambda c: _update(update_client, mailmap, c))
        .transform(consume)
    )
    return mutation_msg.bind(lambda _: result)


def _start(
    connection: DbConnection,
    table: TableId,
    namespace: str,
    mailmap: Maybe[Mailmap],
) -> Cmd[None]:
    sql_client_1 = new_client(connection, LOG.getChild("sql_client_1"))
    sql_client_2 = new_client(connection, LOG.getChild("sql_client_2"))
    client = sql_client_1.map(lambda q: Client.new(q, table))
    client2 = sql_client_2.map(lambda q: Client.new(q, table))
    return client.bind(
        lambda c1: client2.bind(
            lambda c2: amend_users(c1, c2, namespace, mailmap)
        )
    )


def start(
    db_id: DatabaseId,
    creds: Credentials,
    table: TableId,
    namespace: str,
    mailmap: Maybe[Mailmap],
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
            unsafe_unwrap(_start(conn, table, namespace, mailmap))
        finally:
            unsafe_unwrap(conn.close())

    return Cmd.from_cmd(_action)