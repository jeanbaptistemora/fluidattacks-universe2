# pylint: disable=invalid-name
"""
Migrate event comments to "integrates_vms" table.
"""

from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Key,
)
from dataloaders import (
    get_new_context,
)
from db_model import (
    finding_comments as finding_comments_model,
    TABLE,
)
from db_model.finding_comments.types import (
    FindingComment,
)
from dynamodb import (
    keys,
    operations,
    operations_legacy as ops_legacy,
)
from dynamodb.types import (
    Item,
)
import logging
import logging.config
from newutils.finding_comments import (
    format_finding_comments,
)
from organizations import (
    domain as orgs_domain,
)
from settings import (
    LOGGING,
)
import time
from typing import (
    Any,
)

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")
COMMENTS_TABLE = "fi_finding_comments"


async def get_finding_by_id(finding_id: str) -> dict[str, Any]:
    primary_key = keys.build_key(
        facet=TABLE.facets["finding_metadata"],
        values={"id": finding_id},
    )

    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["finding_metadata"],),
        limit=1,
        table=TABLE,
    )

    return response.items[0] if response.items else {}


async def process_comment(
    all_active_group_names: tuple[str, ...], item: Item
) -> None:
    comment_type = item["comment_type"]
    if comment_type == "event":
        return

    finding_id = item["finding_id"]
    finding = await get_finding_by_id(finding_id)
    if not finding:
        return

    group_name = finding["group_name"]
    if group_name not in all_active_group_names:
        return

    finding_comment: FindingComment = format_finding_comments(item)
    await finding_comments_model.add(finding_comment=finding_comment)


async def main() -> None:
    loaders = get_new_context()
    comments_scanned: list[Item] = await ops_legacy.scan(
        table=COMMENTS_TABLE, scan_attrs={}
    )
    all_active_group_names = await orgs_domain.get_all_active_group_names(
        loaders
    )
    LOGGER_CONSOLE.info(
        "All comments", extra={"extra": {"scanned": len(comments_scanned)}}
    )

    await collect(
        tuple(
            process_comment(all_active_group_names, item)
            for item in comments_scanned
        ),
        workers=128,
    )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC"
    )
    print(f"{execution_time}\n{finalization_time}")
