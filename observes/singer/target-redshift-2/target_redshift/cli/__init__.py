# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from . import (
    _from_s3,
    _upload,
)
from ._core import (
    CmdContext,
)
import click
from redshift_client.sql_client.connection import (
    Credentials,
    DatabaseId,
)
from typing import (
    Any,
)


@click.group()  # type: ignore[misc]
@click.option(
    "--db-name",
    envvar="REDSHIFT_DATABASE",
    required=True,
)
@click.option(
    "--db-host",
    envvar="REDSHIFT_HOST",
    required=True,
)
@click.option(
    "--db-port",
    envvar="REDSHIFT_PORT",
    type=int,
    required=True,
)
@click.option(
    "--db-user",
    envvar="REDSHIFT_USER",
    required=True,
)
@click.option(
    "--db-passwd",
    envvar="REDSHIFT_PASSWORD",
    required=True,
)
@click.pass_context
def main(  # type: ignore[misc]
    ctx: Any,
    db_name: str,
    db_host: str,
    db_port: int,
    db_user: str,
    db_passwd: str,
) -> None:
    if "--help" not in click.get_os_args():
        ctx.obj = CmdContext(  # type: ignore[misc]
            DatabaseId(db_name, db_host, db_port),
            Credentials(db_user, db_passwd),
        )


main.add_command(_upload.destroy_and_upload)
main.add_command(_from_s3.from_s3)
