import click
from fa_purity import (
    Cmd,
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
from utils_logger_2 import (
    start_session,
)


@click.command()  # type: ignore[misc]
@click.option(  # type: ignore[misc]
    "--bucket", required=True, type=str, help="s3 bucket name"
)
@click.option(  # type: ignore[misc]
    "--prefix", required=True, type=str, help="Prefix for uploaded s3 files"
)
@click.option(  # type: ignore[misc]
    "--str-limit",
    required=False,
    default=-1,
    type=int,
    help="Max number of chars in a str field. Default -1 (no limit)",
)
@click.option(  # type: ignore[misc]
    "--bypass-input",
    is_flag=True,
    type=bool,
    help="std output stream = std input stream",
)
def main(
    bucket: str, prefix: str, str_limit: int, bypass_input: bool
) -> NoReturn:
    cmd: Cmd[None] = start_session() + loader.main(
        bucket, prefix, stdin_buffer(bypass_input), str_limit
    )
    cmd.compute()
