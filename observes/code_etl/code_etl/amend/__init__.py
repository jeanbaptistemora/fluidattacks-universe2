# pylint: skip-file

from code_etl.amend.actions import (
    update_stamp,
)
from code_etl.amend.core import (
    amend_commit_stamp_users,
)
from code_etl.client import (
    decoder,
    namespace_data,
)
from code_etl.mailmap import (
    Mailmap,
)
from code_etl.objs import (
    CommitStamp,
)
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
from returns.functions import (
    raise_exception,
)
from returns.io import (
    IO,
)
from returns.maybe import (
    Maybe,
)


def amend_users(
    client: Client,
    table: TableID,
    namespace: str,
    mailmap: Maybe[Mailmap],
    hash_2: bool,
) -> IO[None]:
    data = namespace_data(client, table, namespace).map(
        lambda i: i.map(lambda r: r.bind(decoder.decode_commit_table_row))
    )
    for io_r in data:
        io_r.map(lambda r: r.alt(raise_exception).unwrap()).map(
            lambda c: update_stamp(
                client,
                table,
                c,
                mailmap.map(
                    lambda mmap: amend_commit_stamp_users(mmap, c, hash_2)
                ).value_or(c),
            )
            if isinstance(c, CommitStamp)
            else IO(None)
        )
    return IO(None)


def start(
    db_id: DatabaseID,
    creds: Credentials,
    table: TableID,
    namespace: str,
    mailmap: Maybe[Mailmap],
    hash_2: bool,
) -> IO[None]:
    client = ClientFactory().from_creds(db_id, creds)
    return amend_users(client, table, namespace, mailmap, hash_2)
