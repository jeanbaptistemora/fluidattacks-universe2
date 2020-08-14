"""Fluid Forces CLI module."""
# Standard library
from typing import (
    Any,
)
import sys
import re
from io import TextIOWrapper

# Third parties libraries
import jose.jwt
import jose.exceptions
import click

# Local imports
from forces import entrypoint
from forces.utils.aio import block

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
                 "You can generate one at https://fluidattacks.com/integrates"
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
@click.option('--repo-path', default=('.'))
def main(token: str,  # pylint: disable=too-many-arguments
         verbose: int,
         strict: bool,
         output: TextIOWrapper,
         repo_path: str) -> None:
    """Main function"""
    group = get_group_from_email(decode_token(token)['user_email'])
    result = block(entrypoint,
                   token=token,
                   group=group,
                   verbose_level=verbose,
                   strict=strict,
                   output=output,
                   repo_path=repo_path)
    sys.exit(result)
