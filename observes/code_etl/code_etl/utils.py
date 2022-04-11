from datetime import (
    datetime,
)
from fa_purity import (
    Cmd,
)
import logging
from os import (
    environ,
)
from redshift_client.sql_client.connection import (
    Credentials,
    DatabaseId,
)
from typing import (
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
