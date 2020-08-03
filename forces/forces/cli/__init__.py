"""Fluid Forces CLI module."""
# Standard library
import sys
from io import TextIOWrapper

# Third parties libraries
import jose.jwt
import jose.exceptions
import click

# Local imports
from forces import entrypoint
from forces.utils.aio import block


class IntegratesToken(click.ParamType):
    """Represents a integrates api token."""
    name = "integrates_token"

    def convert(self, value: str, param, ctx) -> str:  # type: ignore
        """Validate token integrity."""
        try:
            jose.jwt.decode(value, key='', options={
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
        except jose.exceptions.JOSEError:
            self.fail(
                ("Please verify the validity of your integrates api token.\n"
                 "You can generate one at https://fluidattacks.com/integrates"
                 ),
                param,
                ctx)

        return value


@click.command(name='forces')
@click.option(
    '--token',
    required=True,
    help='Integrates valid token',
    type=IntegratesToken())
@click.option('--group', required=True, help='Name of group')
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
         group: str,
         verbose: int,
         strict: bool,
         output: TextIOWrapper,
         repo_path: str) -> None:
    """Main function"""
    result = block(entrypoint,
                   token=token,
                   group=group,
                   verbose_level=verbose,
                   strict=strict,
                   output=output,
                   repo_path=repo_path)
    sys.exit(result)
