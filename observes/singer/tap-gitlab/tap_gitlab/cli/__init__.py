from ._streams import (
    project_stream,
    Streams,
)
import click
from datetime import (
    timedelta,
)
from fa_purity import (
    Cmd,
    Maybe,
)
import re
from tap_gitlab import (
    cleaner,
    executor,
)
from tap_gitlab.api2 import (
    Credentials as Credentials2,
)
from tap_gitlab.api2.project import (
    ProjectId,
)
from tap_gitlab.api2.project.jobs import (
    JobClient,
)
from tap_gitlab.api.auth import (
    Credentials,
)
from tap_gitlab.streams import (
    SupportedStreams,
)
from typing import (
    NoReturn,
    Optional,
    Tuple,
)


class InvalidURI(Exception):
    pass


def _extract_s3_ids(url: str) -> Tuple[str, str]:
    pattern = re.compile("s3:\/\/(.+)")
    path = pattern.match(url)
    if path:
        parts = path.group(1).split("/", 1)
        return (parts[0], parts[1])
    raise InvalidURI()


@click.command()
@click.option("--api-key", type=str, required=True)
@click.option("--project", type=str, required=True)
@click.option(
    "--state",
    type=str,
    default=None,
    help="json file S3 URI; e.g. s3://mybucket/folder/state.json",
)
@click.option("--max-pages", type=int, default=1000)
@click.option("--all-streams", is_flag=True)
@click.argument(
    "name",
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
    state: Optional[str],
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
    _state = Maybe.from_optional(state)
    if name:
        executor.defautl_stream(
            creds, name, project, max_pages, _state.map(_extract_s3_ids)
        )
    if all_streams:
        raise NotImplementedError()


@click.command()
@click.option("--api-key", type=str, required=True)
@click.option("--project", type=str, required=True)
@click.option("--threshold", type=int, default=1, help="in hours")
@click.option("--start-page", type=int, default=1)
@click.option("--dry-run", is_flag=True)
def clean_stuck_jobs(
    api_key: str, project: str, threshold: int, start_page: int, dry_run: bool
) -> NoReturn:
    # utility to find and cancel stuck jobs
    creds = Credentials2(api_key)
    client = JobClient.new(creds, ProjectId.from_raw_str(project))
    cmd: Cmd[None] = cleaner.clean_stuck_jobs(
        client, start_page, timedelta(hours=threshold), dry_run
    )
    cmd.compute()


@click.command("stream")
@click.option("--api-key", type=str, required=True)
@click.option("--project", type=str, required=True)
@click.argument(
    "stream",
    type=click.Choice([x.value for x in iter(Streams)], case_sensitive=False),
    required=False,
    default=None,
)
def stream_v2(api_key: str, project: str, stream: str) -> NoReturn:
    project_stream(api_key, project, stream).compute()


@click.group()
def v2() -> None:
    # cli group entrypoint
    pass


v2.add_command(stream_v2)


@click.group()
def main() -> None:
    # cli group entrypoint
    pass


main.add_command(v2)
main.add_command(stream)
main.add_command(clean_stuck_jobs)
