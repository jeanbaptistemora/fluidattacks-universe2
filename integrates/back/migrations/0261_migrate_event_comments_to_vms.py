# pylint: disable=invalid-name
"""
Migrate event comments to "integrates_vms" table.

Execution Time:    2022-08-19 at 06:00:40 UTC
Finalization Time: 2022-08-19 at 06:02:03 UTC
"""

from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from custom_exceptions import (
    EventNotFound,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    event_comments as event_comments_model,
)
from db_model.event_comments.types import (
    EventComment,
)
from db_model.events.types import (
    Event,
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
from newutils.event_comments import (
    format_event_comments,
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
        await loaders.event.load(event_id)
        return True
    except EventNotFound:
        return False


async def process_comment(
    loaders: Dataloaders, all_active_group_names: tuple[str, ...], item: Item
) -> None:
    comment_type = item["comment_type"]
    event_id = item["finding_id"]
    if comment_type == "event" and await exists(loaders, event_id):
        event: Event = await loaders.event.load(event_id)
        group_name = event.group_name
        if (
            not await groups_domain.exists(loaders, group_name)
            or group_name not in all_active_group_names
        ):
            return

        event_comment: EventComment = format_event_comments(item)
        await event_comments_model.add(event_comment=event_comment)


async def main() -> None:
    loaders = get_new_context()
    scan_attrs = {"FilterExpression": Attr("comment_type").eq("event")}
    comments_scanned: list[Item] = await ops_legacy.scan(
        table=COMMENTS_TABLE, scan_attrs=scan_attrs
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
