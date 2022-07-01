import click
import tap_json
from typing import (
    Optional,
)


@click.command(help="Deduce singer schemas from singer records or raw JSON")
@click.option(
    "--date-formats",
    type=str,
    required=False,
    default="",
    help="A string of formats separated by comma, extends RFC3339",
)
@click.option(
    "--only-schema",
    is_flag=True,
    help="Emit only determined schemas",
)
@click.option(
    "--schema-cache",
    default=None,
    help="Path to directory containing previously determined schemas",
)
def main(
    date_formats: Optional[str], only_schema: bool, schema_cache: Optional[str]
) -> None:
    tap_json.main(
        date_formats.split(",") if date_formats else [],
        only_schema,
        schema_cache,
    )
