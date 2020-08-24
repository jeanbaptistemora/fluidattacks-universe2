# Standard libraries
import sys

# Third party libraries
from aioextensions import (
    run,
)
import click

# Local libraries
from utils.function import (
    shield,
)
from utils.logs import (
    blocking_log,
)


@click.command(
    help='Deterministic vulnerability life-cycle reporting and closing tool.',
)
@click.argument(
    'config',
    type=click.Path(
        allow_dash=False,
        dir_okay=False,
        exists=True,
        file_okay=True,
        readable=True,
        resolve_path=True,
    ),
)
@click.option(
    '--debug',
    help='Enable debug mode.',
    is_flag=True,
)
@click.option(
    '--token',
    envvar='INTEGRATES_API_TOKEN',
    help='Integrates API token.',
    show_envvar=True,
)
def dispatch(
    config: str,
    debug: bool,
    token: str,
) -> None:
    """Read the execution flags from the CLI and dispatch them to Skims."""
    success: bool = run(
        main_wrapped(
            config=config,
            debug=debug,
            token=token,
        ),
        debug=debug,
    )

    blocking_log('info', 'Success: %s', success)

    sys.exit(0 if success else 1)


@shield(on_error_return=False)
async def main_wrapped(
    config: str,
    debug: bool,
    token: str,
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
    import core.entrypoint

    success: bool = await core.entrypoint.main(
        config=config,
        debug=debug,
        token=token,
    )

    return success
