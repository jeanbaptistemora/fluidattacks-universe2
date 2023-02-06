"""Fluid Forces CLI module."""

# pylint: disable=import-outside-toplevel


import aioextensions
from aioextensions import (
    run,
)
import click
from forces.model import (
    ForcesConfig,
    KindEnum,
)
from forces.utils.bugs import (
    configure_bugsnag,
)
from forces.utils.env import (
    ENDPOINT,
    guess_environment,
)
from forces.utils.function import (
    shield,
)
from forces.utils.logs import (
    blocking_log,
    log,
    log_banner,
    LogInterface,
    rich_log,
)
from forces.utils.strict_mode import (
    choose_min_breaking_severity,
)
from io import (
    TextIOWrapper,
)
import re
import sys
import textwrap
from time import (
    sleep,
)

# Constants
USER_PATTERN = r"forces.(?P<group>\w+)@fluidattacks.com"


def is_forces_user(email: str) -> bool:
    """Ensure that is an forces user."""
    return bool(re.match(USER_PATTERN, email))


def get_group_from_email(email: str) -> str:
    return re.match(USER_PATTERN, email).group("group")  # type: ignore


def show_banner() -> None:
    """Show forces banner"""
    name: str = (
        "[default on red]  [/][bold default on red]››[/]"
        "[bold red on white]› [/][italic bold red] Fluid [white]Attacks[/][/]"
    )
    motto: str = "[italic bold white] We [red]hack[/] your software[/]"
    logo: str = f"""
    [default on white]        [/]
    [default on white]  [/]{name}
    [default on white]  [/][default on red]    [/][red on white]  [/]{motto}
    [default on white]        [/]"""
    console_header: str = textwrap.dedent(
        r"""
        [bright_green]      ____            _____           ____
             / __ \___ _   __/ ___/___  _____/ __ \____  _____
            / / / / _ \ | / /\__ \/ _ \/ ___/ / / / __ \/ ___/
           / /_/ /  __/ |/ /___/ /  __/ /__/ /_/ / /_/ (__  )
          /_____/\___/|___//____/\___/\___/\____/ .___/____/
                                               /_/[/]
        """
    )
    log_header: str = "[bold green]D E V S E C O P S[/]"
    rich_log(logo)
    rich_log(rich_msg=console_header, log_to=LogInterface.CONSOLE)
    log_banner(log_header)


@click.command(name="forces")
@click.option("--token", required=True, help="Integrates valid token")
@click.option(
    "-v",
    "--verbose",
    count=True,
    default=3,
    required=False,
    type=click.IntRange(min=1, max=4),
)
@click.option(
    "--output",
    "-O",
    metavar="FILE",
    type=click.File("w", encoding="utf-8"),
    help="Save output in FILE",
    required=False,
)
@click.option("--strict/--lax")
@click.option("--dynamic", required=False, is_flag=True)
@click.option("--static", required=False, is_flag=True)
@click.option("--repo-path", default=("."))
@click.option(
    "--repo-name",
    required=False,
    default=None,
    help="Name of the repository in which it is running",
)
@click.option(
    "--breaking",
    required=False,
    default=None,
    help="""Minimum CVSS score of a still vulnerable area to break the
    build in strict mode. This setting overrides the global minimum breaking
    severity set by your organization in ARM""",
    type=click.FloatRange(min=0.0, max=10.0),
)
# pylint: disable=too-many-arguments
def main(
    token: str,
    verbose: int,
    strict: bool,
    output: TextIOWrapper,
    repo_path: str,
    dynamic: bool,
    static: bool,
    repo_name: str,
    breaking: float,
) -> None:
    """Main function"""
    kind = "all"
    if dynamic:
        kind = "dynamic"
    elif static:
        kind = "static"

    # Use only one worker,
    # some customers are experiencing threads exhaustion
    # and we suspect it could be this
    try:
        assert not aioextensions.PROCESS_POOL.initialized
        assert not aioextensions.THREAD_POOL.initialized
        aioextensions.PROCESS_POOL.initialize(max_workers=1)
        aioextensions.THREAD_POOL.initialize(max_workers=1)

        result: int = 1
        for _ in range(6):
            try:
                result = run(
                    main_wrapped(
                        token=token,
                        verbose=verbose,
                        strict=strict,
                        output=output,
                        repo_path=repo_path,
                        kind=kind,
                        repo_name=repo_name,
                        local_breaking=breaking,
                    )
                )
                break
            except RuntimeError as err:
                blocking_log(
                    "warning", "An error ocurred: %s. Retrying...", err
                )
                sleep(10.0)

        sys.exit(result)
    finally:
        aioextensions.PROCESS_POOL.shutdown(wait=True)
        aioextensions.THREAD_POOL.shutdown(wait=True)


@shield(on_error_return=1)
async def main_wrapped(  # pylint: disable=too-many-arguments, too-many-locals
    token: str,
    verbose: int,
    strict: bool,
    output: TextIOWrapper,
    repo_path: str,
    kind: str,
    repo_name: str,
    local_breaking: float,
) -> int:
    from forces import (
        entrypoint,
    )
    from forces.apis.integrates.api import (
        get_forces_user_and_org_data,
    )

    (
        organization,
        group,
        global_brk_severity,
        vuln_grace_period,
    ) = await get_forces_user_and_org_data(api_token=token)
    if not organization or not group:
        await log("warning", "Please make sure that you use a forces user")
        return 1

    configure_bugsnag(group=group or "")
    show_banner()
    if guess_environment() == "development":
        await log("info", "The agent is running in dev mode")
        await log("info", f"The agent is pointing to {ENDPOINT}")

    strictness = "strict" if strict else "lax"
    await log(
        "info",
        f"Running the DevSecOps agent in [bright_yellow]{strictness}[/] mode",
    )
    await log(
        "info", f"Running the DevSecOps agent in [bright_yellow]{kind}[/] kind"
    )

    if kind == "dynamic":
        kind_chg = KindEnum.DYNAMIC
    else:
        kind_chg = KindEnum.STATIC if kind == "static" else KindEnum.ALL
    config = ForcesConfig(
        organization=organization,
        group=group,
        kind=kind_chg,
        output=output,
        repository_path=repo_path,
        repository_name=repo_name,
        strict=strict,
        verbose_level=verbose,
        breaking_severity=choose_min_breaking_severity(
            global_brk_severity=global_brk_severity,
            local_brk_severity=local_breaking,
        ),
        grace_period=vuln_grace_period if vuln_grace_period is not None else 0,
    )
    return await entrypoint(
        token=token,
        config=config,
    )


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main(prog_name="forces")
