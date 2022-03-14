from enum import (
    Enum,
)
import os
from redshift_client.sql_client.connection import (
    Credentials,
    DatabaseId,
)
from typing import (
    Tuple,
)


class EnvVarPrefix(Enum):
    SOURCE = "SOURCE"
    TARGET = "TARGET"


def from_env(prefix: EnvVarPrefix) -> Tuple[DatabaseId, Credentials]:
    creds = Credentials(
        os.environ[f"{prefix.value}_DB_USER"],
        os.environ[f"{prefix.value}_DB_PASSWORD"],
    )
    db = DatabaseId(
        os.environ[f"{prefix.value}_DB_NAME"],
        os.environ[f"{prefix.value}_DB_HOST"],
        int(os.environ[f"{prefix.value}_DB_PORT"]),
    )
    return (db, creds)
