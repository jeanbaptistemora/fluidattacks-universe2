# Standard libraries
import json
# Third party libraries
import click
# Local libraries
from zoho_crm_etl import auth
from zoho_crm_etl.auth import Credentials


@click.command()
@click.argument('auth_file', type=click.File('r'))
def gen_refresh_token(auth_file):
    # Manual refresh token generation, see:
    # https://www.zoho.com/crm/developer/docs/api/v2/auth-request.html
    print(
        auth.generate_refresh_token(
            auth.to_credentials(auth_file)
        )
    )


@click.group()
def main():
    pass


main.add_command(gen_refresh_token)
