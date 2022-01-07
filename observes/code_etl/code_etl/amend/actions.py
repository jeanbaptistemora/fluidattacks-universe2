# pylint: skip-file

from code_etl.client import (
    delta_update,
    encoder,
)
from code_etl.objs import (
    CommitStamp,
)
import logging
from postgres_client.client import (
    Client,
)
from postgres_client.ids import (
    TableID,
)
from returns.io import (
    IO,
)

LOG = logging.getLogger(__name__)


def update_stamp(
    client: Client, table: TableID, old: CommitStamp, new: CommitStamp
) -> IO[None]:
    if old != new:
        LOG.info("delta update %s", old.commit.commit_id)
        return delta_update(
            client, table, encoder.from_stamp(old), encoder.from_stamp(new)
        )
    return IO(None)
