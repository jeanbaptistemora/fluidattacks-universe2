from ._core import (
    CmdContext,
    pass_ctx,
)
import click
from fa_purity import (
    Cmd,
    Maybe,
)
from target_redshift.from_s3 import (
    FromS3Executor,
)
from typing import (
    NoReturn,
)


@click.command()  # type: ignore[misc]
@click.option(
    "--schema-name",
    type=str,
    required=True,
    help="Schema name in your warehouse",
)
@click.option(
    "--bucket",
    type=str,
    required=True,
    help="S3 bucket name",
)
@click.option(
    "--prefix",
    type=str,
    required=True,
    help="S3 target files prefix",
)
@click.option(
    "--role",
    type=str,
    required=True,
    help="arn of an iam role for S3 access",
)
@click.option(
    "--wlm-queue",
    type=str,
    required=False,
    default=None,
    help="redshift wlm queue group for the executed queries",
)
@click.option(
    "--ignore-failed",
    type=bool,
    is_flag=True,
    help="ignore json items that does not decode to a singer message",
)
@pass_ctx
def from_s3(
    ctx: CmdContext,
    schema_name: str,
    bucket: str,
    prefix: str,
    role: str,
    wlm_queue: str | None,
    ignore_failed: bool,
) -> NoReturn:
    executor = FromS3Executor(
        ctx.db_id,
        ctx.creds,
        schema_name,
        bucket,
        prefix,
        role,
        ignore_failed,
        Maybe.from_optional(wlm_queue),
    )
    cmd: Cmd[None] = executor.execute()
    cmd.compute()
