# pylint: skip-file
from __future__ import (
    annotations,
)

import click
from dataclasses import (
    dataclass,
)
from purity.v1 import (
    JsonFactory,
)
from returns.io import (
    IO,
)
from returns.maybe import (
    Maybe,
)
from typing import (
    IO as IOFile,
    Optional,
)


@dataclass(frozen=True)
class Creds:
    key_id: str
    key: str
    region: str

    @staticmethod
    def from_file(file: IOFile[str]) -> Creds:
        data = JsonFactory.load(file)
        return Creds(
            data["AWS_ACCESS_KEY_ID"].to_primitive(str),
            data["AWS_SECRET_ACCESS_KEY"].to_primitive(str),
            data["AWS_DEFAULT_REGION"].to_primitive(str),
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
    return IO(None)


@click.group()
def main() -> None:
    # cli group entrypoint
    pass


main.add_command(stream)
