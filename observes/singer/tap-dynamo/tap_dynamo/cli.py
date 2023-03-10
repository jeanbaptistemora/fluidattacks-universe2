import click
from fa_purity import (
    Cmd,
    Maybe,
)
from tap_dynamo import (
    extractor,
)
from tap_dynamo.client import (
    Client,
    DynamoConf,
)
from typing import (
    NoReturn,
)
from utils_logger_2 import (
    start_session,
)


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
@click.option(
    "--endpoint-url",
    type=str,
    default=None,
    help="dynamo endpoint url",
)
@click.option(
    "--region-name",
    type=str,
    default=None,
    help="dynamo region name",
)
@click.option(
    "--use-ssl",
    type=bool,
    default=None,
    help="dynamo use ssl",
)
@click.option(
    "--verify",
    type=bool,
    default=None,
    help="dynamo verify",
)
def stream(
    tables: str,
    segments: int,
    endpoint_url: str | None,
    region_name: str | None,
    use_ssl: bool | None,
    verify: bool | None,
) -> NoReturn:
    conf = DynamoConf(endpoint_url, region_name, use_ssl, verify)
    cmd: Cmd[None] = start_session() + Client.new_client(
        Maybe.from_value(conf)
    ).bind(
        lambda client: extractor.stream_tables(
            client, tuple(tables.split()), segments
        )
    )
    cmd.compute()


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
def stream_segment(table: str, current: int, total: int) -> NoReturn:
    cmd: Cmd[None] = start_session() + Client.new_client(Maybe.empty()).bind(
        lambda client: extractor.stream_segment(
            client, extractor.TableSegment(table, current, total)
        )
    )
    cmd.compute()


@click.group()
def main() -> None:
    # main cli group
    pass


main.add_command(stream)
main.add_command(stream_segment)
