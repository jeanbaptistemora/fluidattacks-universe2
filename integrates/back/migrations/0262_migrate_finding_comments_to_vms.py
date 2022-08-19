# pylint: disable=invalid-name
"""
Migrate event comments to "integrates_vms" table.
"""

from aioextensions import (
    collect,
    run,
)
from custom_exceptions import (
    FindingNotFound,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    finding_comments as finding_comments_model,
)
from db_model.finding_comments.types import (
    FindingComment,
)
from decorators import (
    Finding,
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

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")
COMMENTS_TABLE = "fi_finding_comments"


async def exists(
    loaders: Dataloaders,
    event_id: str,
) -> bool:
    try:
        await loaders.finding.load(event_id)
        return True
    except FindingNotFound:
        return False


async def process_comment(
    loaders: Dataloaders, all_active_group_names: tuple[str, ...], item: Item
) -> None:
    comment_type = item["comment_type"]
    finding_id = item["finding_id"]
    if comment_type != "event" and await exists(loaders, finding_id):
        finding: Finding = await loaders.finding.load(finding_id)
        group_name = finding.group_name
        if (
            not await groups_domain.exists(loaders, group_name)
            or group_name not in all_active_group_names
        ):
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
            process_comment(loaders, all_active_group_names, item)
            for item in comments_scanned
        ),
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
