from datetime import (
    datetime,
)
from fa_purity import (
    Cmd,
    FrozenList,
)
from fa_purity.cmd import (
    unsafe_unwrap,
)
from fa_purity.cmd.core import (
    CmdUnwrapper,
    new_cmd,
)
import logging
from os import (
    environ,
)
from pathos.threading import (  # type: ignore[import]
    ThreadPool,
)
from redshift_client.sql_client import (
    DbConnection,
)
from redshift_client.sql_client.connection import (
    Credentials,
    DatabaseId,
)
from typing import (
    Callable,
    TypeVar,
)

LOG = logging.getLogger(__name__)
COMMIT_HASH_SENTINEL: str = "-" * 40
DATE_SENTINEL: datetime = datetime.utcfromtimestamp(0)
DATE_NOW: datetime = datetime.utcnow()

DB_ID = DatabaseId(
    environ["REDSHIFT_DATABASE"],
    environ["REDSHIFT_HOST"],
    int(environ["REDSHIFT_PORT"]),
)
DB_CREDS = Credentials(
    environ["REDSHIFT_USER"],
    environ["REDSHIFT_PASSWORD"],
)

_T = TypeVar("_T")


def log_info(log: logging.Logger, msg: str, *args: str) -> Cmd[None]:
    return Cmd.from_cmd(lambda: log.info(msg, *args))


def wrap_connection(
    connection: DbConnection, action: Callable[[DbConnection], Cmd[None]]
) -> Cmd[None]:
    """Ensures that connection is closed regardless of action errors"""

    def _action() -> None:
        try:
            unsafe_unwrap(action(connection))
        finally:
            unsafe_unwrap(connection.close())

    return Cmd.from_cmd(_action)


def cmds_in_threads(cmds: FrozenList[Cmd[None]]) -> Cmd[None]:
    def _action(act: CmdUnwrapper) -> None:
        pool = ThreadPool()  # type: ignore[misc]
        LOG.debug("Concurrent action started!")
        pool.map(  # type: ignore[misc]
            act.unwrap,
            cmds,
        )

    return new_cmd(_action)
