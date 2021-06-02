# pylint: disable=import-outside-toplevel
from aioextensions import (
    run,
)
import click
from functools import (
    partial,
)
import logging
from model import (
    core_model,
)
import sys
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
REPO = partial(
    click.argument,
    "repository",
    type=click.Path(
        allow_dash=False,
        dir_okay=True,
        exists=True,
        file_okay=False,
        readable=True,
        resolve_path=True,
    ),
)

FINDING_CODE = partial(
    click.option,
    "--finding-code",
    help=f"One of: {', '.join(core_model.FindingEnum.__members__)}.",
    metavar="CODE",
    show_choices=False,
    type=click.Choice(tuple(core_model.FindingEnum.__members__)),
)
FINDING_TITLE = partial(
    click.option,
    "--finding-title",
    help="Finding title.",
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
    if debug:
        set_level(logging.DEBUG)


@cli.command(help="Get a group's language.", name="language")
@GROUP(required=True)
@TOKEN(required=True)
def cli_language(
    group: str,
    token: str,
) -> None:
    success: bool = run(
        cli_language_wrapped(
            group=group,
            token=token,
        )
    )
    sys.exit(0 if success else 1)


@cli.command(help="Queue a Skims execution on AWS Batch.", name="queue")
@FINDING_CODE()
@FINDING_TITLE()
@GROUP(required=True)
@click.option(
    "--urgent",
    help="Queue the job with the highest priority.",
    is_flag=True,
)
def cli_queue(
    finding_code: Optional[str],
    finding_title: Optional[str],
    group: str,
    urgent: bool,
) -> None:
    success: bool = run(
        cli_queue_wrapped(
            finding_code=finding_code,
            finding_title=finding_title,
            group=group,
            urgent=urgent,
        )
    )
    sys.exit(0 if success else 1)


@cli.command(help="Update vulnerability locations.", name="rebase")
@GROUP(required=True)
@NAMESPACE(required=True)
@REPO()
@TOKEN(required=True)
def cli_rebase(
    group: str,
    namespace: str,
    repository: str,
    token: str,
) -> None:
    success: bool = run(
        cli_rebase_wrapped(
            group=group,
            namespace=namespace,
            repository=repository,
            token=token,
        ),
    )

    log_blocking("info", "Success: %s", success)

    sys.exit(0 if success else 1)


@cli.command(help="Perform vulnerability detection.", name="scan")
@CONFIG()
@GROUP()
@TOKEN()
def cli_scan(
    config: str,
    group: Optional[str],
    token: Optional[str],
) -> None:
    CTX.config = None

    start_time: float = time()
    success: bool = run(
        cli_scan_wrapped(
            config=config,
            group=group,
            token=token,
        ),
    )

    log_blocking("info", "Success: %s", success)

    if guess_environment() == "production":
        log_to_remote_blocking(
            execution_seconds=f"{time() - start_time}",
            msg="Success" if success else "Failure",
            severity="info" if success else "error",
        )

    sys.exit(0 if success else 1)


@shield(on_error_return=False)
async def cli_language_wrapped(
    group: str,
    token: str,
) -> bool:
    import core.language

    initialize_bugsnag()
    add_bugsnag_data(
        group=group,
        token=token,
    )
    return await core.language.main(
        group=group,
        token=token,
    )


@shield(on_error_return=False)
async def cli_queue_wrapped(
    finding_code: Optional[str],
    finding_title: Optional[str],
    group: str,
    urgent: bool,
) -> bool:
    import core.queue

    initialize_bugsnag()
    add_bugsnag_data(
        finding_code=str(finding_code),
        finding_title=str(finding_title),
        group=group,
        urgent=str(urgent),
    )
    success: bool = await core.queue.main(
        finding_code=finding_code,
        finding_title=finding_title,
        group=group,
        urgent=urgent,
    )

    return success


@shield(on_error_return=False)
async def cli_rebase_wrapped(
    group: str,
    namespace: str,
    repository: str,
    token: str,
) -> bool:
    import core.rebase

    initialize_bugsnag()
    add_bugsnag_data(
        group=group,
        namespace=namespace,
        token=token,
    )
    success: bool = await core.rebase.main(
        group=group,
        namespace=namespace,
        repository=repository,
        token=token,
    )

    return success


@shield(on_error_return=False)
async def cli_scan_wrapped(
    config: str,
    group: Optional[str],
    token: Optional[str],
) -> bool:
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
