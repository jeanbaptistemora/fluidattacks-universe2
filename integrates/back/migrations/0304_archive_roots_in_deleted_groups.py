# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=invalid-name
"""
From deleted groups, archive roots metadata in redshift and
remove all items from vms.

Execution Time:    2022-10-26 at 17:45:07 UTC
Finalization Time: 2022-10-26 at 22:24:44 UTC
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
    roots as roots_model,
)
from db_model.roots.get import (  # type: ignore
    get_group_roots_items,
)
from decorators import (
    retry_on_exceptions,
)
from dynamodb.types import (
    Item,
)
import logging
import logging.config
from organizations import (
    domain as orgs_domain,
)
import psycopg2
from redshift import (  # type: ignore
    roots as redshift_roots,
)
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def _remove_root(
    item: Item,
) -> None:
    root_id = item["pk"].split("#")[1]
    await roots_model.remove(root_id=root_id)


@retry_on_exceptions(
    exceptions=(psycopg2.OperationalError,),
    sleep_seconds=1,
)
async def _archive_root_items(items: tuple[Item, ...]) -> None:
    await redshift_roots.insert_batch_roots(items=items)


async def _process_group(
    group_name: str,
    progress: float,
) -> None:
    items = await get_group_roots_items(group_name=group_name)
    if not items:
        return
    await _archive_root_items(items=items)
    await collect(
        tuple(_remove_root(item) for item in items),
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
    await collect(
        tuple(
            _process_group(
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
