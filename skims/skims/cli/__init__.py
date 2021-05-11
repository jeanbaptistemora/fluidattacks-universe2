# Standard libraries
from functools import (
    partial,
)
import sys
from time import (
    time,
)
from typing import (
    Optional,
)

# Third party libraries
from aioextensions import (
    run,
)
import click

# Local libraries
from utils.ctx import (
    CTX,
)
from utils.env import (
    guess_environment,
)
from utils.function import (
    shield,
)
from utils.logs import (
    log_blocking,
    log_to_remote_blocking,
)
from utils.bugs import (
    add_bugsnag_data,
    initialize_bugsnag,
)

# Reusable components
CONFIG = partial(
    click.argument,
    "config",
    type=click.Path(
        allow_dash=False,
        dir_okay=False,
        exists=True,
        file_okay=True,
        readable=True,
        resolve_path=True,
    ),
)
GROUP = partial(
    click.option,
    "--group",
    envvar="INTEGRATES_GROUP",
    help="Integrates group to which results will be persisted.",
    show_envvar=True,
)
NAMESPACE = partial(
    click.option,
    "--namespace",
    envvar="INTEGRATES_NAMESPACE",
    help="Integrates namespace.",
    show_envvar=True,
)
TOKEN = partial(
    click.option,
    "--token",
    envvar="INTEGRATES_API_TOKEN",
    help="Integrates API token.",
    show_envvar=True,
)


@click.group(
    help="Deterministic vulnerability life-cycle reporting and closing tool.",
)
@click.option(
    "--debug",
    help="Enable debug mode.",
    is_flag=True,
)
def cli(
    debug: bool,
) -> None:
    CTX.debug = debug


@cli.command(help="Load a config file and perform vulnerability detection.")
@CONFIG()
@GROUP()
@TOKEN()
def scan(
    config: str,
    group: Optional[str],
    token: Optional[str],
) -> None:
    CTX.config = None

    start_time: float = time()
    success: bool = run(
        scan_wrapped(
            config=config,
            group=group,
            token=token,
        ),
        debug=False,
    )

    log_blocking("info", "Success: %s", success)

    if guess_environment() == "production":
        log_to_remote_blocking(
            execution_seconds=f"{time() - start_time}",
            msg="Success" if success else "Failure",
            severity="info" if success else "error",
        )

    sys.exit(0 if success else 1)


@cli.command(help="Update vulnerability locations at Integrates.")
@GROUP(required=True)
@NAMESPACE(required=True)
@TOKEN(required=True)
def rebase(
    group: str,
    namespace: str,
    token: str,
) -> None:
    success: bool = run(
        rebase_wrapped(
            group=group,
            namespace=namespace,
            token=token,
        ),
    )

    log_blocking("info", "Success: %s", success)

    sys.exit(0 if success else 1)


@shield(on_error_return=False)
async def rebase_wrapped(
    group: str,
    namespace: str,
    token: str,
) -> bool:
    # Import here to handle gracefully any errors it may throw
    # pylint: disable=import-outside-toplevel
    import core.rebase

    initialize_bugsnag()
    add_bugsnag_data(
        group=group,
        token="set" if token else "",
    )
    success: bool = await core.rebase.main(
        group=group,
        namespace=namespace,
        token=token,
    )

    return success


@shield(on_error_return=False)
async def scan_wrapped(
    config: str,
    group: Optional[str],
    token: Optional[str],
) -> bool:
    """Wrap the main function in order to handle gracefully its errors.

    If any error is raised in `main` this function:
    - catches the error
    - returns False (which triggers an exit-code 1)
    - report errors to bugsnag
    - report errors to the user via a friendly message in the console

    Otherwise returns True and trigger an exit-code 0.
    """
    # Import here to handle gracefully any errors it may throw
    # pylint: disable=import-outside-toplevel
    import core.scan

    initialize_bugsnag()
    add_bugsnag_data(
        config=config,
        group=group or "",
        token="set" if token else "",
    )
    success: bool = await core.scan.main(
        config=config,
        group=group,
        token=token,
    )

    return success


if __name__ == "__main__":
    cli(  # pylint: disable=no-value-for-parameter,unexpected-keyword-arg
        prog_name="skims",
    )
