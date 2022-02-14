# pylint: skip-file
import click
from fa_purity.maybe import (
    Maybe,
)
from purity.v1 import (
    JsonFactory,
)
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
    IO,
    NoReturn,
    Optional,
)


@click.command()
@click.option("--auth", type=click.File("r"), required=True)
@click.option("--conf", type=click.File("r"), required=False)
@click.option("--table", type=str, required=False)
def stream(  # type: ignore[misc]
    auth: IO[str], conf: Optional[IO[str]], table: Optional[str]
) -> NoReturn:
    creds = Creds.from_file(auth)
    _conf = Maybe.from_optional(conf)
    tables = _conf.map(
        lambda c: JsonFactory.load(c)["tables"].to_list_of(str)
    ).or_else_call(lambda: [Maybe.from_optional(table).unwrap()])
    client = new_client(creds)
    stream_tables(client, tuple(tables)).compute()


@click.group()
def main() -> None:
    # cli group entrypoint
    pass


main.add_command(stream)
