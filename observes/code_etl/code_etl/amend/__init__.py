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
from postgres_client.client import (
    Client,
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
    client: Client, table: TableID, namespace: str, mailmap: Maybe[Mailmap]
) -> IO[None]:
    data = namespace_data(client, table, namespace).map(
        lambda i: i.map(lambda r: r.bind(decoder.decode_commit_stamp))
    )
    for io_r in data:
        io_r.map(lambda r: r.alt(raise_exception).unwrap()).map(
            lambda c: update_stamp(
                client,
                table,
                c,
                mailmap.map(
                    lambda mmap: amend_commit_stamp_users(mmap, c)
                ).value_or(c),
            )
        )
    return IO(None)
