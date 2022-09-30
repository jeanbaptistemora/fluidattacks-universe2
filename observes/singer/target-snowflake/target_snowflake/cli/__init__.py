# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from . import (
    _upload,
)
from ._core import (
    CmdContext,
)
import click
from fa_purity import (
    Maybe,
)
import sys
from target_snowflake.snowflake_client.sql_client import (
    Credentials,
    DatabaseId,
    Identifier,
)
from typing import (
    Any,
    Optional,
)


@click.group()  # type: ignore[misc]
@click.option(  # type: ignore[misc]
    "--user",
    envvar="SNOWFLAKE_USER",
    required=True,
)
@click.option(  # type: ignore[misc]
    "--password",
    envvar="SNOWFLAKE_PASSWORD",
    required=True,
)
@click.option(  # type: ignore[misc]
    "--account",
    envvar="SNOWFLAKE_ACCOUNT",
    required=True,
)
@click.option(  # type: ignore[misc]
    "--db-name",
    envvar="SNOWFLAKE_DB",
    required=True,
)
@click.option(  # type: ignore[misc]
    "--db-host",
    required=False,
    default=None,
)
@click.option(  # type: ignore[misc]
    "--db-port",
    type=int,
    required=False,
    default=None,
)
@click.pass_context  # type: ignore[misc]
def main(
    ctx: Any,
    db_name: str,
    db_host: Optional[str],
    db_port: Optional[int],
    user: str,
    password: str,
    account: str,
) -> None:
    if "--help" not in sys.argv[1:]:
        ctx.obj = CmdContext(  # type: ignore[misc]
            DatabaseId(Identifier.from_raw(db_name), db_host, db_port),
            Credentials(user, password, account),
        )


main.add_command(_upload.destroy_and_upload)
