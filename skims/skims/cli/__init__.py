# pylint: disable=import-outside-toplevel
from aioextensions import (
    run,
)
import click
from ctx import (
    CTX,
    LEGAL,
)
from functools import (
    partial,
)
import logging
import sys
import textwrap
from time import (
    time,
)
from typing import (
    Optional,
)
from utils.bugs import (
    add_bugsnag_data,
    initialize_bugsnag,
)
from utils.env import (
    guess_environment,
)
from utils.function import (
    shield_blocking,
)
from utils.logs import (
    log_blocking,
    log_to_remote_blocking,
    set_level,
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


@click.group(
    help="Deterministic vulnerability life-cycle reporting and closing tool.",
    epilog=textwrap.dedent(
        f"""
            For legal information read {LEGAL}
        """
    ),
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
    if debug:
        set_level(logging.DEBUG)


@cli.command(help="Perform vulnerability detection.", name="scan")
@CONFIG()
@GROUP()
def cli_scan(
    config: str,
    group: Optional[str],
) -> None:
    CTX.config = None

    start_time: float = time()
    success: bool = cli_scan_wrapped(
        config=config,
        group=group,
    )

    log_blocking("info", "Success: %s", success)

    if guess_environment() == "production" and not success:
        log_to_remote_blocking(
            execution_seconds=f"{time() - start_time}",
            msg="Failure",
            severity="error",
        )

    sys.exit(0 if success else 1)


@shield_blocking(on_error_return=False)
def cli_scan_wrapped(
    config: str,
    group: Optional[str],
) -> bool:
    import core.scan

    initialize_bugsnag()
    add_bugsnag_data(
        config=config,
        group=group or "",
    )
    success: bool = run(
        core.scan.main(
            config=config,
            group=group,
        )
    )

    return success


if __name__ == "__main__":
    cli(  # pylint: disable=no-value-for-parameter
        prog_name="skims",
    )
