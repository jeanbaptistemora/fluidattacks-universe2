# pylint: disable=invalid-name
"""
Rename modified_commit by last_commit and commit_author by last_author for toe
lines.

Execution Time:     2022-02-10 at 19:06:09 UTC
Finalization Time:  2022-02-10 at 22:13:05 UTC

Execution Time:     2022-02-10 at 22:58:17 UTC
Finalization Time:  2022-02-10 at 23:21:02 UTC
"""

from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Key,
)
from db_model import (
    TABLE,
)
from decorators import (
    retry_on_exceptions,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.exceptions import (
    UnavailabilityError,
)
from dynamodb.types import (
    Item,
)
from groups import (
    domain as groups_domain,
)
import logging
import logging.config
from settings import (
    LOGGING,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER_CONSOLE = logging.getLogger("console")


@retry_on_exceptions(
    exceptions=(UnavailabilityError,),
    sleep_seconds=3,
)
async def process_lines(item: Item) -> None:
    metadata_key = keys.build_key(
        facet=TABLE.facets["toe_lines_metadata"],
        values={
            "filename": item["filename"],
            "group_name": item["group_name"],
            "root_id": item["root_id"],
        },
    )
    metadata_item: Item = {}
    if item.get("commit_author") is not None:
        metadata_item["commit_author"] = None
        metadata_item["last_author"] = item["commit_author"]

    if item.get("modified_commit") is not None:
        metadata_item["modified_commit"] = None
        metadata_item["last_commit"] = item["modified_commit"]

    if metadata_item:
        await operations.update_item(
            item=metadata_item,
            key=metadata_key,
            table=TABLE,
        )


async def process_group(group_name: str, progress: float) -> None:
    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(f"GROUP#{group_name}")
            & Key(key_structure.sort_key).begins_with("LINES#")
        ),
        facets=(TABLE.facets["toe_lines_metadata"],),
        index=None,
        table=TABLE,
    )
    await collect(
        tuple(process_lines(item) for item in response.items), workers=1000
    )
    LOGGER_CONSOLE.info(
        "Group updated",
        extra={
            "extra": {
                "group_name": group_name,
                "progress": progress,
            }
        },
    )


async def main() -> None:
    group_names = tuple(
        group["project_name"]
        for group in await groups_domain.get_all(attributes=["project_name"])
    )
    group_names_len = len(group_names)
    await collect(
        tuple(
            process_group(group_name, count / group_names_len)
            for count, group_name in enumerate(group_names)
        ),
        workers=3,
    )


if __name__ == "__main__":
    run(main())
