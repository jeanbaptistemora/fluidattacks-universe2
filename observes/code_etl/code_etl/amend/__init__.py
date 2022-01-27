from code_etl.amend.actions import (
    update_stamp,
)
from code_etl.amend.core import (
    AmendUsers,
)
from code_etl.client import (
    decoder,
)
from code_etl.client.v2 import (
    namespace_data,
)
from code_etl.mailmap import (
    Mailmap,
)
from code_etl.objs import (
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
from purity.v2.cmd import (
    Cmd,
)
from purity.v2.maybe import (
    Maybe,
)
from purity.v2.stream.transform import (
    consume,
)
from typing import (
    Union,
)

LOG = logging.getLogger(__name__)


def _update(
    client: Client,
    table: TableID,
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
        return update_stamp(client, table, item, fixed)
    return Cmd.from_cmd(lambda: None)


def amend_users(
    client: Client,
    table: TableID,
    namespace: str,
    mailmap: Maybe[Mailmap],
) -> Cmd[None]:
    start_msg = Cmd.from_cmd(lambda: LOG.info("Getting data stream..."))
    mutation_msg = Cmd.from_cmd(lambda: LOG.info("Mutation started"))
    data = namespace_data(client, table, namespace).map(
        lambda s: s.map(lambda r: r.bind(decoder.decode_commit_table_row))
    )
    result = data.bind(
        lambda s: s.map(lambda r: r.unwrap())
        .map(lambda c: _update(client, table, mailmap, c))
        .transform(consume)
    )
    return (
        start_msg.bind(lambda _: data)
        .bind(lambda _: mutation_msg)
        .bind(lambda _: result)
    )


def start(
    db_id: DatabaseID,
    creds: Credentials,
    table: TableID,
    namespace: str,
    mailmap: Maybe[Mailmap],
) -> Cmd[None]:
    client = ClientFactory().from_creds(db_id, creds)
    return amend_users(client, table, namespace, mailmap)
