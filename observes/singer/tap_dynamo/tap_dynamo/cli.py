import click
from tap_dynamo.auth import (
    Creds,
)
from tap_dynamo.client import (
    new_client,
)
from tap_dynamo.extractor import (
    stream_tables,
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
def stream(  # type: ignore[misc]
    creds: Creds, tables: str, segments: int
) -> NoReturn:
    client = new_client(creds)
    stream_tables(client, tuple(tables.split()), segments).compute()


@click.group()
@click.option("--key-id", type=str, envvar="AWS_ACCESS_KEY_ID")
@click.option("--secret-id", type=str, envvar="AWS_SECRET_ACCESS_KEY")
@click.option("--region", type=str, envvar="AWS_DEFAULT_REGION")
@click.pass_context
def main(ctx: Any, key_id: str, secret_id: str, region: str) -> None:
    if "--help" not in click.get_os_args():
        ctx.obj = Creds(key_id, secret_id, region)


main.add_command(stream)
