import click
import sys
from tap_dynamo import (
    extractor,
)
from tap_dynamo.auth import (
    Creds,
)
from tap_dynamo.client import (
    new_client,
)
from typing import (
    Any,
    NoReturn,
)

pass_creds = click.make_pass_decorator(Creds)


@click.command()
@click.option(
    "--tables",
    type=str,
    required=True,
    help="space separated dynamoDB source tables",
)
@click.option(
    "--segments",
    type=int,
    default=1,
    help="tables segmentation for fast extraction",
)
@pass_creds
def stream(creds: Creds, tables: str, segments: int) -> NoReturn:
    client = new_client(creds)
    extractor.stream_tables(client, tuple(tables.split()), segments).compute()


@click.command()
@click.option(
    "--table",
    type=str,
    required=True,
    help="dynamoDB source table",
)
@click.option(
    "--current",
    type=int,
    required=True,
    help="# of table segment",
)
@click.option(
    "--total",
    type=int,
    required=True,
    help="total table segments",
)
@pass_creds
def stream_segment(
    creds: Creds, table: str, current: int, total: int
) -> NoReturn:
    client = new_client(creds)
    seg = extractor.TableSegment(table, current, total)
    extractor.stream_segment(client, seg).compute()


@click.group()
@click.option("--key-id", type=str, envvar="AWS_ACCESS_KEY_ID")
@click.option("--secret-id", type=str, envvar="AWS_SECRET_ACCESS_KEY")
@click.option("--region", type=str, envvar="AWS_DEFAULT_REGION")
@click.pass_context
def main(ctx: Any, key_id: str, secret_id: str, region: str) -> None:
    if "--help" not in sys.argv[1:]:
        ctx.obj = Creds(key_id, secret_id, region)


main.add_command(stream)
main.add_command(stream_segment)
