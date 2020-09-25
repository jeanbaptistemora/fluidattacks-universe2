"""Fluid Forces CLI module."""
# Standard library
from typing import (
    Any,
)
import sys
import re
import textwrap
from io import TextIOWrapper
from importlib.metadata import version

# Third parties libraries
import jose.jwt
import jose.exceptions
import click
from aioextensions import run

# Local imports
from forces import entrypoint
from forces.utils.bugs import configure_bugsnag
from forces.utils.function import shield
from forces.utils.logs import blocking_log

# Constants
USER_PATTERN = r'forces.(?P<group>\w+)@fluidattacks.com'


def is_forces_user(email: str) -> bool:
    """Ensure that is an forces user."""
    return bool(re.match(USER_PATTERN, email))


def get_group_from_email(email: str) -> str:
    return re.match(USER_PATTERN, email).group('group')  # type: ignore


def decode_token(token: str) -> Any:
    return jose.jwt.decode(token,
                           key='',
                           options={
                               'verify_signature': False,
                               'verify_aud': True,
                               'verify_iat': True,
                               'verify_exp': True,
                               'verify_nbf': True,
                               'verify_iss': True,
                               'verify_sub': True,
                               'verify_jti': True,
                               'verify_at_hash': True,
                               'leeway': 0,
                           })


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
        try:
            token_data = decode_token(value)
            if not is_forces_user(token_data.get('user_email')):
                self.fail(("Ensure that you use an forces user"), param, ctx)
        except jose.exceptions.JOSEError:
            self.fail(
                ("Please verify the validity of your integrates api token.\n"
                 "You can generate one at https://integrates.fluidattacks.com"
                 ),
                param,
                ctx,
            )

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
    group = get_group_from_email(decode_token(token)['user_email'])
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

    blocking_log('info', 'Success: %s', result == 0)
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
    return await entrypoint(
        token=token,
        group=group,
        verbose_level=verbose,
        strict=strict,
        output=output,
        repo_path=repo_path,
        kind=kind,
        repo_name=repo_name,
    )
