# pylint: skip-file

import click
import re
from returns.maybe import (
    Maybe,
)
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
    Tuple,
)


class InvalidURL(Exception):
    pass


def _extract_s3_ids(url: str) -> Tuple[str, str]:
    pattern = re.compile("s3:\/\/(.+)")
    path = pattern.match(url)
    if path:
        parts = path.group(0).split("/", 1)
        return (parts[0], parts[1])
    raise InvalidURL()


@click.command()
@click.option("--api-key", type=str, required=True)
@click.option("--project", type=str, required=True)
@click.option(
    "--state",
    type=str,
    default=None,
    help="json file S3 bucket URL; e.g. s3://mybucket/folder/state.json",
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


@click.group()
def main() -> None:
    # cli group entrypoint
    pass


main.add_command(stream)
