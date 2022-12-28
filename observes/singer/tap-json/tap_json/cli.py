import click
import tap_json
from typing import (
    Optional,
)


@click.command(help="Deduce singer schemas from singer records or raw JSON")  # type: ignore[misc]
@click.option(  # type: ignore[misc]
    "--date-formats",
    type=str,
    required=False,
    default="",
    help="A string of formats separated by comma, extends RFC3339",
)
@click.option(  # type: ignore[misc]
    "--schema-cache",
    is_flag=True,
    help="Use custom schema folder as cache, do not auto determine it",
)
@click.option(  # type: ignore[misc]
    "--schema-folder",
    default=None,
    help="Path to directory for input/output of the schemas",
)
@click.option(  # type: ignore[misc]
    "--not-dump-records",
    is_flag=True,
    help="Do not stream records",
)
def main(
    date_formats: Optional[str],
    schema_cache: bool,
    schema_folder: Optional[str],
    not_dump_records: bool,
) -> None:
    tap_json.main(
        date_formats.split(",") if date_formats else [],
        schema_cache,
        schema_folder,
        not not_dump_records,
    )
