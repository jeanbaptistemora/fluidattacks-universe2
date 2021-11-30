# pylint: skip-file
import click
from purity.v1 import (
    JsonFactory,
)
from returns.io import (
    IO,
)
from returns.maybe import (
    Maybe,
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
    IO as IOFile,
    Optional,
)


@click.command()
@click.option("--auth", type=click.File("r"), required=True)
@click.option("--conf", type=click.File("r"), required=False)
@click.option("--table", type=str, required=False)
def stream(
    auth: IOFile[str], conf: Optional[IOFile[str]], table: Optional[str]
) -> IO[None]:
    creds = Creds.from_file(auth)
    _conf = Maybe.from_optional(conf)
    tables = _conf.map(
        lambda c: JsonFactory.load(c)["tables"].to_list_of(str)
    ).value_or([Maybe.from_optional(table).unwrap()])
    client = new_client(creds)
    return stream_tables(client, tuple(tables))


@click.group()
def main() -> None:
    # cli group entrypoint
    pass


main.add_command(stream)
