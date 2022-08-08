import click
from fa_purity import (
    Cmd,
)
from fa_purity.utils import (
    raise_exception,
)
from target_s3 import (
    loader,
)
from target_s3.in_buffer import (
    stdin_buffer,
)
from typing import (
    NoReturn,
)


@click.command()  # type: ignore[misc]
@click.option(  # type: ignore[misc]
    "--bucket", required=True, type=str, help="s3 bucket name"
)
@click.option(  # type: ignore[misc]
    "--prefix", required=True, type=str, help="Prefix for uploaded s3 files"
)
def main(bucket: str, prefix: str) -> NoReturn:
    cmd: Cmd[None] = loader.main(bucket, prefix, stdin_buffer())
    cmd.compute()
