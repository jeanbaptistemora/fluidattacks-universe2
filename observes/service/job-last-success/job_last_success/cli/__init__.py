from . import (
    _sub_cmds,
)
from ._core import (
    CmdContext,
)
import click
from fa_purity.pure_iter.factory import (
    from_flist,
)
from redshift_client.sql_client.connection import (
    Credentials,
    DatabaseId,
)
import sys
from typing import (
    Any,
    Optional,
)


@click.group()  # type: ignore[misc]
@click.option(  # type: ignore[misc]
    "--db-name",
    envvar="REDSHIFT_DATABASE",
    required=False,
)
@click.option(  # type: ignore[misc]
    "--db-host",
    envvar="REDSHIFT_HOST",
    required=False,
)
@click.option(  # type: ignore[misc]
    "--db-port",
    envvar="REDSHIFT_PORT",
    type=int,
    required=False,
)
@click.option(  # type: ignore[misc]
    "--db-user",
    envvar="REDSHIFT_USER",
    required=False,
)
@click.option(  # type: ignore[misc]
    "--db-passwd",
    envvar="REDSHIFT_PASSWORD",
    required=False,
)
@click.pass_context  # type: ignore[misc]
def main(
    ctx: Any,
    db_name: Optional[str],
    db_host: Optional[str],
    db_port: Optional[int],
    db_user: Optional[str],
    db_passwd: Optional[str],
) -> None:
    if "--help" in sys.argv[1:]:
        ctx.obj = CmdContext(  # type: ignore[misc]
            DatabaseId("", "", 0),
            Credentials("", ""),
        )
        return
    if "--help" not in sys.argv[1:] and (
        db_name is not None
        and db_host is not None
        and db_port is not None
        and db_user is not None
        and db_passwd is not None
    ):
        ctx.obj = CmdContext(  # type: ignore[misc]
            DatabaseId(db_name, db_host, db_port),
            Credentials(db_user, db_passwd),
        )
    else:
        missing = (
            from_flist(
                (
                    ("db_name", db_name),
                    ("db_host", db_host),
                    ("db_port", db_port),
                    ("db_user", db_user),
                    ("db_passwd", db_passwd),
                )
            )
            .filter(lambda t: t[1] is None)
            .map(lambda x: x[0])
        )
        raise ValueError(f"Missing db args i.e. {missing.to_list()}")


main.add_command(_sub_cmds.single_job)
main.add_command(_sub_cmds.compound_job)
