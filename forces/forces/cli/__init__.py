"""Fluid Forces CLI module."""
# Standard library
import sys
from io import TextIOWrapper

# Third parties libraries
import jose.jwt
import jose.exceptions
import oyaml as yaml
import click

# Local imports
from forces.apis.integrates import (
    set_api_token,
)
from forces.report import process


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
    type=click.File('w'),
    help='save output in FILE',
    required=False)
@click.option('--strict/--lax')
def main(token: str, group: str, verbose: int, strict: bool,
         output: TextIOWrapper) -> None:
    """Main function"""
    set_api_token(token)

    report = process(group, verbose)
    yaml_report = yaml.dump(report)

    if output:
        output.write(yaml_report)
    else:
        print(yaml_report)
    if strict:
        if report['summary']['open'] > 0:
            sys.exit(1)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
