# Standard libraries
# Third party libraries
import click

# Local libraries
from timedoctor_tokens import core


@click.command()
@click.option("--creds", type=str, required=True)
def code_grant_page(creds: str) -> None:
    core.code_grant_page(creds)


@click.command()
@click.option("--creds", type=str, required=True)
@click.option("--grant-code", type=str, required=True)
def get_and_update_token(creds: str, grant_code: str) -> None:
    core.get_and_update_token(creds, grant_code)


@click.command()
@click.option("--creds", type=str, required=True)
def update_token(creds: str) -> None:
    core.timedoctor_refresh(creds)


@click.group()
def main() -> None:
    # cli group entrypoint
    pass


main.add_command(code_grant_page)
main.add_command(get_and_update_token)
main.add_command(update_token)
