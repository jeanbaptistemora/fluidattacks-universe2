from ._core import (
    CmdContext,
    pass_ctx,
)
import boto3
import click
from fa_purity import (
    Cmd,
)
import logging
from mypy_boto3_s3 import (
    S3Client,
    S3ServiceResource,
)
from redshift_client.id_objs import (
    SchemaId,
)
from redshift_client.schema.client import (
    SchemaClient,
)
from redshift_client.sql_client import (
    new_client,
)
from redshift_client.sql_client.connection import (
    connect,
    DbConnection,
    IsolationLvl,
)
from redshift_client.table.client import (
    TableClient,
)
from target_redshift import (
    loader,
)
from target_redshift.loader import (
    LoadingStrategy,
    S3Handler,
)
from typing import (
    NoReturn,
)

LOG = logging.getLogger(__name__)


def _new_s3_client() -> Cmd[S3Client]:
    return Cmd.from_cmd(lambda: boto3.client("s3"))


def _new_s3_resource() -> Cmd[S3ServiceResource]:
    return Cmd.from_cmd(lambda: boto3.resource("s3"))


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
@pass_ctx
def from_s3(
    ctx: CmdContext,
    schema_name: str,
    bucket: str,
    prefix: str,
    role: str,
) -> NoReturn:
    _schema = SchemaId(schema_name)

    def _main(conn: DbConnection) -> Cmd[None]:
        client = new_client(conn, LOG)
        schema_client = client.map(SchemaClient)
        table_client = client.map(TableClient)
        strategy = schema_client.map(lambda s: LoadingStrategy(_schema, s))

        def _upload(target: SchemaId) -> Cmd[None]:
            handler = client.bind(
                lambda db: _new_s3_client().bind(
                    lambda c: _new_s3_resource().map(
                        lambda r: S3Handler(
                            target, c, r, db, bucket, prefix, role
                        )
                    )
                )
            )
            return table_client.bind(
                lambda tc: handler.bind(
                    lambda h: loader.from_s3(target, tc, h)
                )
            )

        return strategy.bind(lambda ls: ls.main(_upload))

    connection = connect(ctx.db_id, ctx.creds, False, IsolationLvl.AUTOCOMMIT)
    cmd: Cmd[None] = connection.bind(_main)
    cmd.compute()
