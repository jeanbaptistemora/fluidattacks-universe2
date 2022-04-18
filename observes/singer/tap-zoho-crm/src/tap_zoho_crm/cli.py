import click
from tap_zoho_crm import (
    auth,
    etl,
)
from tap_zoho_crm.auth import (
    Credentials,
)
from typing import (
    AnyStr,
    IO,
)


@click.command()
@click.argument("crm_auth_file", type=click.File("r"))
def gen_refresh_token(crm_auth_file: IO[AnyStr]) -> None:
    # Manual refresh token generation, see:
    # https://www.zoho.com/crm/developer/docs/api/v2/auth-request.html
    crm_creds: Credentials = auth.to_credentials(crm_auth_file)
    print(auth.generate_refresh_token(crm_creds))


@click.command()
def revoke_token() -> None:
    # Manual refresh token revoke
    print(auth.revoke_refresh_token())


@click.command()
@click.argument("db_auth_file", type=click.File("r"))
def init_db(db_auth_file: IO[AnyStr]) -> None:
    db_id, db_creds = auth.to_db_credentials(db_auth_file)
    etl.initialize(db_id, db_creds)


@click.command()
@click.argument("crm_auth_file", type=click.File("r"))
@click.argument("db_auth_file", type=click.File("r"))
def create_jobs(crm_auth_file: IO[AnyStr], db_auth_file: IO[AnyStr]) -> None:
    crm_creds: Credentials = auth.to_credentials(crm_auth_file)
    db_id, db_creds = auth.to_db_credentials(db_auth_file)
    etl.creation_phase(crm_creds, db_id, db_creds)


@click.command()
@click.argument("crm_auth_file", type=click.File("r"))
@click.argument("db_auth_file", type=click.File("r"))
def stream(crm_auth_file: IO[AnyStr], db_auth_file: IO[AnyStr]) -> None:
    crm_creds: Credentials = auth.to_credentials(crm_auth_file)
    db_id, db_creds = auth.to_db_credentials(db_auth_file)
    etl.start_streamer(crm_creds, db_id, db_creds)


@click.group()
def main() -> None:
    # cli group entrypoint
    pass


main.add_command(create_jobs)
main.add_command(gen_refresh_token)
main.add_command(init_db)
main.add_command(revoke_token)
main.add_command(stream)
