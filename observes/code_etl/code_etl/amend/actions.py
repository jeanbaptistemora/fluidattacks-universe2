# pylint: skip-file

from code_etl.client import (
    delta_update,
    encoder,
)
from code_etl.objs import (
    CommitStamp,
)
from postgres_client.client import (
    Client,
)
from postgres_client.ids import (
    TableID,
)
from returns.io import (
    IO,
)


def update_stamp(
    client: Client, table: TableID, old: CommitStamp, new: CommitStamp
) -> IO[None]:
    return delta_update(
        client, table, encoder.from_stamp(old), encoder.from_stamp(new)
    )
