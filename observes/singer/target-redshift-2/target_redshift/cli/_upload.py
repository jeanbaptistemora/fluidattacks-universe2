from ._core import (
    CmdContext,
    pass_ctx,
)
import click
from fa_purity import (
    Cmd,
    Maybe,
)
from redshift_client.id_objs import (
    SchemaId,
)
from target_redshift._utils import (
    S3FileObjURI,
)
from target_redshift.destroy_upload import (
    DestroyUploadExecutor,
)
from target_redshift.loader import (
    SingerHandlerOptions,
)
from typing import (
    NoReturn,
    Optional,
)


@click.command()  # type: ignore[misc]
@click.option(
    "-s",
    "--schema-name",
    type=str,
    required=True,
    help="Schema name in your warehouse",
)
@click.option(
    "--records-limit",
    type=int,
    required=False,
    default=1000000,
    help="Max # of records per group",
)
@click.option(
    "--records-per-query",
    type=int,
    required=False,
    default=1000,
    help="Max # of records per sql query",
)
@click.option(
    "--threads",
    type=int,
    required=False,
    default=1000,
    help="# of threads for query upload",
)
@click.option(
    "--truncate",
    type=bool,
    is_flag=True,
    help="Truncate records that exceed column size?",
)
@click.option(
    "--s3-state",
    type=str,
    required=False,
    default=None,
    help="S3 file obj URI to upload the state; e.g. s3://mybucket/folder/state.json",
)
@click.option(
    "--persistent-tables",
    type=str,
    required=False,
    default=None,
    help="set of table names (separated by comma) that would not be recreated but will also receive new data",
)
@click.option(
    "--ignore-failed",
    type=bool,
    is_flag=True,
    help="ignore json items that does not decode to a singer message",
)
@pass_ctx
def destroy_and_upload(
    ctx: CmdContext,
    schema_name: str,
    records_limit: int,
    truncate: bool,
    records_per_query: int,
    threads: int,
    s3_state: Optional[str],
    persistent_tables: Optional[str],
    ignore_failed: bool,
) -> NoReturn:
    target = SchemaId(schema_name)
    options = SingerHandlerOptions(
        truncate,
        records_per_query,
        threads,
    )
    state = (
        Maybe.from_optional(s3_state)
        .map(S3FileObjURI.from_raw)
        .map(lambda r: r.unwrap())
    )
    persistent = (
        Maybe.from_optional(persistent_tables)
        .map(lambda raw: frozenset(raw.split(",")))
        .bind_optional(lambda f: f if f else None)
    )
    cmd: Cmd[None] = DestroyUploadExecutor(
        ctx.db_id,
        ctx.creds,
        target,
        options,
        records_limit,
        state,
        persistent,
        ignore_failed,
    ).execute()
    cmd.compute()
