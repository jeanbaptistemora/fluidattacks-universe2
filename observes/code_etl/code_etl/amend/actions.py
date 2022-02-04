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
)
from fa_purity.maybe import (
    Maybe,
)
from fa_purity.stream.transform import (
    consume,
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
    client: Client,
    namespace: str,
    mailmap: Maybe[Mailmap],
) -> Cmd[None]:
    start_msg = Cmd.from_cmd(lambda: LOG.info("Getting data stream..."))
    mutation_msg = Cmd.from_cmd(lambda: LOG.info("Mutation started"))
    data = client.namespace_data(namespace)
    result = data.bind(
        lambda s: s.map(lambda r: r.unwrap())
        .map(lambda c: _update(client, mailmap, c))
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
    client = Client(ClientFactory().from_creds(db_id, creds), table)
    return amend_users(client, namespace, mailmap)
