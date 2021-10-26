"""Fluid Forces CLI module."""

# pylint: disable=import-outside-toplevel


from aioextensions import (
    run,
)
import click
from forces.utils.bugs import (
    configure_bugsnag,
)
from forces.utils.function import (
    shield,
)
from forces.utils.logs import (
    CONSOLE,
    log,
)
from forces.utils.model import (
    ForcesConfig,
    KindEnum,
)
from io import (
    TextIOWrapper,
)
import re
import sys
import textwrap
from typing import (
    Optional,
)

# Constants
USER_PATTERN = r"forces.(?P<group>\w+)@fluidattacks.com"


def is_forces_user(email: str) -> bool:
    """Ensure that is an forces user."""
    return bool(re.match(USER_PATTERN, email))


def get_group_from_email(email: str) -> str:
    return re.match(USER_PATTERN, email).group("group")  # type: ignore


def show_banner() -> None:
    """Show forces banner."""
    # The name and motto may come with closing markup tags from other parts of
    # the banner, this is done to avoid the wrath of the linter, but if any
    # modifications are needed, just paste them back and refac away
    name = "› [/][italic bold red] Fluid [bold white]Attacks[/][/]"
    motto = "[italic bold white] We [bold red]hack[/] your software[/]"
    header = textwrap.dedent(
        rf"""
         [red on red]  ‎ ‎ ‎ ‎ ‎‎  ‎[/]
         [red on red]  [/][bold red on white]‎  ››[/][bold white on red]{name}
         [red on red]  [/][white on white]   ‎ [/][white on red]  [/]{motto}
         [red on red]   ‎‎   ‎ ‎ [/]
        [bold green]
              ____            _____           ____
             / __ \___ _   __/ ___/___  _____/ __ \____  _____
            / / / / _ \ | / /\__ \/ _ \/ ___/ / / / __ \/ ___/
           / /_/ /  __/ |/ /___/ /  __/ /__/ /_/ / /_/ (__  )
          /_____/\___/|___//____/\___/\___/\____/ .___/____/
                                               /_/[/]
        """
    )
    CONSOLE.log(header)


@click.command(name="forces")
@click.option("--token", required=True, help="Integrates valid token")
@click.option("-v", "--verbose", count=True, default=3, required=False)
@click.option(
    "--output",
    "-O",
    metavar="FILE",
    type=click.File("w", encoding="utf-8"),
    help="save output in FILE",
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
    help="name of the repository in which it is running",
)  # pylint: disable=too-many-arguments
def main(
    token: str,
    verbose: int,
    strict: bool,
    output: TextIOWrapper,
    repo_path: str,
    dynamic: bool,
    static: bool,
    repo_name: str,
) -> None:
    """Main function"""
    kind = "all"
    if dynamic:
        kind = "dynamic"
    elif static:
        kind = "static"

    result = run(
        main_wrapped(
            token=token,
            verbose=verbose,
            strict=strict,
            output=output,
            repo_path=repo_path,
            kind=kind,
            repo_name=repo_name,
        )
    )

    sys.exit(result)


@shield(on_error_return=1)
async def main_wrapped(  # pylint: disable=too-many-arguments
    token: str,
    verbose: int,
    strict: bool,
    output: TextIOWrapper,
    repo_path: str,
    kind: str,
    repo_name: str,
) -> int:
    from forces import (
        entrypoint,
    )
    from forces.apis.integrates.api import (
        get_forces_user,
    )

    group: Optional[str] = await get_forces_user(api_token=token)
    if not group:
        await log("warning", "Ensure that you use an forces user")
        return 1

    configure_bugsnag(group=group or "")
    show_banner()

    striccness = "strict" if strict else "lax"
    start_msg: str = "Running DevSecOps agent"
    await log("info", f"{start_msg} in {striccness} mode")
    await log("info", f"{start_msg} in {kind} kind")
    if repo_name:
        await log(
            "info",
            f"{start_msg} for vulnerabilities in the repo: {repo_name}",
        )
    else:
        await log(
            "warning",
            (
                "If the repository name is not specified, it will run on all "
                "the existing repositories in ASM"
            ),
        )

    config = ForcesConfig(
        group=group,
        kind=KindEnum.DYNAMIC
        if kind == "dynamic"
        else (KindEnum.STATIC if kind == "static" else KindEnum.ALL),
        output=output,
        repository_path=repo_path,
        repository_name=repo_name,
        strict=strict,
        verbose_level=verbose,
    )
    return await entrypoint(
        token=token,
        config=config,
    )


if __name__ == "__main__":
    main(  # pylint: disable=no-value-for-parameter,unexpected-keyword-arg
        prog_name="forces"
    )
