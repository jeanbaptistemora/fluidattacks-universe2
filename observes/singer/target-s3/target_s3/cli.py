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
    "--bucket", required=True, type=str, help="s3 bucket URI"
)
@click.option(  # type: ignore[misc]
    "--prefix", required=True, type=str, help="Prefix for uploaded s3 files"
)
def main(bucket: str, prefix: str) -> NoReturn:
    cmd: Cmd[None] = stdin_buffer().bind(
        lambda r: r.map(
            lambda d: loader.main(bucket, prefix, d).bind(
                lambda r: r.alt(raise_exception).unwrap()
            )
        )
        .alt(raise_exception)
        .unwrap()
    )
    cmd.compute()
