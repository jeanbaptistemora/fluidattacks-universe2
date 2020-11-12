"""Fluid Forces CLI module."""
# Standard library
from typing import cast
import sys
import re
import textwrap
from io import TextIOWrapper
from importlib.metadata import version

# Third parties libraries
import click
from aioextensions import run

# Local imports
from forces import entrypoint
from forces.utils.bugs import configure_bugsnag
from forces.utils.function import shield
from forces.utils.logs import blocking_log
from forces.utils.model import (
    ForcesConfig,
    KindEnum,
)
from forces.apis.integrates.api import get_forces_user

# Constants
USER_PATTERN = r'forces.(?P<group>\w+)@fluidattacks.com'


def is_forces_user(email: str) -> bool:
    """Ensure that is an forces user."""
    return bool(re.match(USER_PATTERN, email))


def get_group_from_email(email: str) -> str:
    return re.match(USER_PATTERN, email).group('group')  # type: ignore


def show_banner() -> None:
    """Show forces banner."""
    header = textwrap.dedent(rf"""
        #     ______
        #    / ____/___  _____________  _____
        #   / /_  / __ \/ ___/ ___/ _ \/ ___/
        #  / __/ / /_/ / /  / /__/  __(__  )
        # /_/    \____/_/   \___/\___/____/
        #
        #  v. {version('forces')}
        #  ___
        # | >>|> fluid
        # |___|  attacks, we hack your software
        #
        """)
    blocking_log('info', '%s', header)


class IntegratesToken(click.ParamType):
    """Represents a integrates api token."""
    name = "integrates_token"

    def convert(self, value: str, param, ctx) -> str:  # type: ignore
        """Validate token integrity."""
        if not run(get_forces_user(api_token=value)):
            self.fail(("Ensure that you use an forces user"), param, ctx)

        # when the new token is implemented, do the validations about it
        return value


@click.command(name='forces')
@click.option(
    '--token',
    required=True,
    help='Integrates valid token',
    type=IntegratesToken())
@click.option('-v', '--verbose', count=True, default=3, required=False)
@click.option(
    '--output',
    '-O',
    metavar='FILE',
    type=click.File('w', encoding="utf-8"),
    help='save output in FILE',
    required=False)
@click.option('--strict/--lax')
@click.option('--dynamic', required=False, is_flag=True)
@click.option('--static', required=False, is_flag=True)
@click.option('--repo-path', default=('.'))
@click.option('--repo-name', required=False, default=None)
def main(token: str,  # pylint: disable=too-many-arguments
         verbose: int,
         strict: bool,
         output: TextIOWrapper,
         repo_path: str,
         dynamic: bool,
         static: bool,
         repo_name: str) -> None:
    """Main function"""
    group: str = cast(str, run(get_forces_user(api_token=token)))
    configure_bugsnag(group=group or '')
    show_banner()
    kind = 'all'
    if dynamic:
        kind = 'dynamic'
    elif static:
        kind = 'static'

    striccness = 'strict' if strict else 'lax'
    blocking_log('info', 'Running forces in %s mode', striccness)
    blocking_log('info', 'Running forces in %s kind', kind)
    if repo_name:
        blocking_log(
            'info',
            f'Ruing forces for vulnerabilities in the repo: {repo_name}')

    result = run(
        main_wrapped(
            group=group,
            token=token,
            verbose=verbose,
            strict=strict,
            output=output,
            repo_path=repo_path,
            kind=kind,
            repo_name=repo_name,
        ))

    sys.exit(result)


@shield(on_error_return=1)
async def main_wrapped(  # pylint: disable=too-many-arguments
    group: str,
    token: str,
    verbose: int,
    strict: bool,
    output: TextIOWrapper,
    repo_path: str,
    kind: str,
    repo_name: str,
) -> int:
    config = ForcesConfig(
        group=group,
        kind=KindEnum.DYNAMIC if kind == 'dynamic' else
        (KindEnum.STATIC if kind == 'static' else KindEnum.ALL),
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
