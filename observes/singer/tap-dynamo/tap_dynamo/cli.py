import click
from fa_purity import (
    Cmd,
)
from tap_dynamo import (
    extractor,
)
from tap_dynamo.client import (
    new_client,
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
def stream(tables: str, segments: int) -> NoReturn:
    cmd: Cmd[None] = start_session() + new_client().bind(
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
    cmd: Cmd[None] = start_session() + new_client().bind(
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
