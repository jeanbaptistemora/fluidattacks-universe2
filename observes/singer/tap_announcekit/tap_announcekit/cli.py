import click
from returns.io import (
    IO,
)
from tap_announcekit.api.auth import (
    Creds,
    PASSWD_ENV_VAR,
    USER_ENV_VAR,
)
from tap_announcekit.api.cli import (
    get_api_schema,
    update_schema,
)
from tap_announcekit.streamer import (
    Streamer,
    SupportedStream,
)
from tap_announcekit.streams.project import (
    ProjectId,
)


@click.command()
@click.option("--user", envvar=USER_ENV_VAR, required=True)
@click.option("--passwd", envvar=PASSWD_ENV_VAR, required=True)
@click.option("--project", type=str, required=True)
@click.argument(
    "strm-name",
    type=click.Choice(
        [x.value for x in iter(SupportedStream)],
        case_sensitive=False,
    ),
    required=True,
)
def stream(strm_name: str, user: str, passwd: str, project: str) -> IO[None]:
    creds = Creds(user, passwd)
    selection = SupportedStream(strm_name)
    streamer = Streamer(creds, selection, ProjectId(project))
    return streamer.start()


@click.group()
def main() -> None:
    # cli group entrypoint
    pass


main.add_command(get_api_schema)
main.add_command(update_schema)
main.add_command(stream)
