import click
from tap_gitlab import (
    executor,
)
from tap_gitlab.api.auth import (
    Credentials,
)
from tap_gitlab.streams import (
    SupportedStreams,
)
from typing import (
    Optional,
)


@click.command()
@click.option("--api-key", type=str, required=True)
@click.option("--project", type=str, required=True)
@click.option("--max-pages", type=int, default=1000)
@click.option("--all-streams", is_flag=True)
@click.option(
    "--name",
    type=click.Choice(
        [x.value for x in iter(SupportedStreams)], case_sensitive=False
    ),
    required=False,
    default=None,
)
def stream(
    name: Optional[str],
    api_key: str,
    project: str,
    max_pages: int,
    all_streams: bool,
) -> None:
    if all_streams and name is not None:
        raise click.BadParameter(
            "Only one `all-streams` or `name` option is accepted, not both"
        )
    if not all_streams and name is None:
        raise click.BadParameter("`name` option is required")

    creds = Credentials(api_key)
    if name:
        executor.emit(creds, name, project, max_pages)
    if all_streams:
        executor.stream_all(creds, project, max_pages)


@click.group()
def main() -> None:
    # cli group entrypoint
    pass


main.add_command(stream)
