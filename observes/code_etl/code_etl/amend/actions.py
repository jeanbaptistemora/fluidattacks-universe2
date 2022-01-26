from code_etl.client import (
    encoder,
)
from code_etl.client.v2 import (
    delta_update,
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
from purity.v2.cmd import (
    Cmd,
)

LOG = logging.getLogger(__name__)


def update_stamp(
    client: Client, table: TableID, old: CommitStamp, new: CommitStamp
) -> Cmd[None]:
    if old != new:
        info = Cmd.from_cmd(
            lambda: LOG.info("delta update %s", old.commit.commit_id)
        )
        return info.bind(
            lambda _: delta_update(
                client, table, encoder.from_stamp(old), encoder.from_stamp(new)
            )
        )
    return Cmd.from_cmd(lambda: LOG.debug("no changes"))
