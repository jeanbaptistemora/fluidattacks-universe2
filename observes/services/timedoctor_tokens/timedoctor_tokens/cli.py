import click
from timedoctor_tokens import (
    core,
)


@click.command()
@click.option("--init-creds", type=str, required=True)
def new_grant_code(init_creds: str) -> None:
    core.code_grant_page(init_creds)


@click.command()
@click.option("--init-creds", type=str, required=True)
def set_init_token(init_creds: str) -> None:
    core.get_and_update_token(init_creds)


@click.command()
@click.option("--creds", type=str, required=True)
def update_token(creds: str) -> None:
    core.timedoctor_refresh(creds)


@click.group()
def main() -> None:
    # cli group entrypoint
    pass


main.add_command(new_grant_code)
main.add_command(set_init_token)
main.add_command(update_token)
