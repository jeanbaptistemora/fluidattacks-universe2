# pylint: disable=invalid-name
"""
Migrate group comments to "integrates_vms" table.

Execution Time:    2022-08-19 at 04:39:46 UTC
Finalization Time: 2022-08-19 at 04:40:58 UTC
"""

from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    group_comments as group_comments_model,
)
from db_model.group_comments.types import (
    GroupComment,
)
from dynamodb import (
    operations_legacy as ops_legacy,
)
from dynamodb.types import (
    Item,
)
from groups import (
    domain as groups_domain,
)
import logging
import logging.config
from newutils.group_comments import (
    format_group_comments,
)
from organizations import (
    domain as orgs_domain,
)
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")
COMMENTS_TABLE = "fi_project_comments"


async def process_comment(
    loaders: Dataloaders, all_active_group_names: tuple[str, ...], item: Item
) -> None:
    group_name = item["project_name"]
    if (
        not await groups_domain.exists(loaders, group_name)
        or group_name not in all_active_group_names
    ):
        return
    group_comment: GroupComment = format_group_comments(item)
    await group_comments_model.add(group_comment=group_comment)


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
            process_comment(loaders, all_active_group_names, item)
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
