import click
from dataclasses import (
    dataclass,
)
from redshift_client.sql_client.connection import (
    Credentials,
    DatabaseId,
)


@dataclass(frozen=True)
class CmdContext:
    db_id: DatabaseId
    creds: Credentials


pass_ctx = click.make_pass_decorator(CmdContext)  # type: ignore[misc]
