# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=invalid-name
"""
From deleted groups, archive events metadata in redshift and
remove all items from vms.

Execution Time:    2022-11-03 at 20:39:34 UTC
Finalization Time: 2022-11-03 at 22:02:21 UTC
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
    events as events_model,
)
from db_model.events.get import (  # type: ignore
    get_group_events_items,
)
from decorators import (
    retry_on_exceptions,
)
from dynamodb.types import (
    Item,
)
from event_comments import (
    domain as event_comments_domain,
)
from events import (
    domain as events_domain,
)
import logging
import logging.config
from organizations import (
    domain as orgs_domain,
)
import psycopg2
from psycopg2.extensions import (
    cursor as cursor_cls,
)
from redshift import (  # type: ignore
    events as redshift_events,
)
from redshift.operations import (
    db_cursor,
)
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def _remove_event(
    group_name: str,
    item: Item,
) -> None:
    event_id = item["pk"].split("#")[1]
    evidence_prefix = f"{group_name}/{event_id}"
    list_evidences = await events_domain.search_evidence(evidence_prefix)
    await collect(
        events_domain.remove_file_evidence(file_name)
        for file_name in list_evidences
    )
    await event_comments_domain.remove_comments(event_id)
    await events_model.remove(event_id=event_id)


@retry_on_exceptions(
    exceptions=(psycopg2.OperationalError,),
    sleep_seconds=1,
)
def _archive_event_items(cursor: cursor_cls, items: tuple[Item, ...]) -> None:
    redshift_events.insert_batch_metadata(cursor=cursor, items=items)


async def _process_group(
    cursor: cursor_cls,
    group_name: str,
    progress: float,
) -> None:
    items = await get_group_events_items(group_name=group_name)
    if not items:
        return
    _archive_event_items(cursor=cursor, items=items)
    await collect(
        tuple(
            _remove_event(group_name=group_name, item=item) for item in items
        ),
        workers=16,
    )
    LOGGER_CONSOLE.info(
        "Group processed",
        extra={
            "extra": {
                "group_name": group_name,
                "len(items)": len(items),
                "progress": round(progress, 2),
            }
        },
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    deleted_groups = await orgs_domain.get_all_deleted_groups(loaders)
    deleted_group_names = sorted([group.name for group in deleted_groups])
    LOGGER_CONSOLE.info(
        "Deleted groups",
        extra={"extra": {"groups_len": len(deleted_group_names)}},
    )
    with db_cursor() as cursor:
        await collect(
            tuple(
                _process_group(
                    cursor=cursor,
                    group_name=group_name,
                    progress=count / len(deleted_group_names),
                )
                for count, group_name in enumerate(deleted_group_names)
            ),
            workers=1,
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
