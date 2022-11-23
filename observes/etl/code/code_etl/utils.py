# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from datetime import (
    datetime,
)
from fa_purity import (
    Cmd,
)
from fa_purity.cmd import (
    unsafe_unwrap,
)
import logging
from os import (
    environ,
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
