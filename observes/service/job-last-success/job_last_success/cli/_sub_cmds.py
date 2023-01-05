from ._core import (
    CmdContext,
    pass_ctx,
)
import click
from fa_purity import (
    Cmd,
)
from job_last_success import (
    core,
)
from job_last_success.conf import (
    COMPOUND_JOBS,
    SINGLE_JOBS,
)
from redshift_client.sql_client import (
    DbConnection,
)
from redshift_client.sql_client.connection import (
    IsolationLvl,
)
from typing import (
    NoReturn,
)


@click.command()  # type: ignore[misc]
@click.option("--job", type=str, required=True)  # type: ignore[misc]
@pass_ctx  # type: ignore[misc]
def single_job(ctx: CmdContext, job: str) -> NoReturn:
    if job in SINGLE_JOBS or job.startswith("skims"):
        cmd: Cmd[None] = core.wrap_connection(
            DbConnection.connect(
                ctx.db_id, ctx.creds, False, IsolationLvl.AUTOCOMMIT
            ),
            lambda c: core.update_single_job(c, job),
        )
        cmd.compute()

    else:
        raise KeyError(f"single job: {job}")


@click.command()  # type: ignore[misc]
@click.option("--job", type=str, required=True)  # type: ignore[misc]
@click.option("--child", type=str, required=True)  # type: ignore[misc]
@pass_ctx  # type: ignore[misc]
def compound_job(ctx: CmdContext, job: str, child: str) -> None:
    if job in COMPOUND_JOBS:
        cmd: Cmd[None] = core.wrap_connection(
            DbConnection.connect(
                ctx.db_id, ctx.creds, False, IsolationLvl.AUTOCOMMIT
            ),
            lambda c: core.update_compound_job(c, job, child),
        )
        cmd.compute()
    else:
        raise KeyError(f"compound job: {job}")
