import click
from tap_announcekit.api.cli import (
    get_api_schema,
    update_schema,
)


@click.group()
def main() -> None:
    # cli group entrypoint
    pass


main.add_command(get_api_schema)
main.add_command(update_schema)
