# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=invalid-name
"""
Archive deleted groups in redshift and remove all related items from vms.

Execution Time:    2022-11-15 at 19:23:56 UTC
Finalization Time: 2022-11-15 at 21:36:03 UTC
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
    groups as groups_model,
)
from db_model.groups.get import (  # type: ignore
    get_group_historic_state_items,
    get_group_item,
    get_group_unreliable_indicators_item,
)
from decorators import (
    retry_on_exceptions,
)
from group_comments import (
    domain as group_comments_domain,
)
from groups import (
    domain as groups_domain,
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
from redshift import (
    groups as redshift_groups,
    operations as redshift_ops,
)
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


@retry_on_exceptions(
    exceptions=(psycopg2.OperationalError,),
    sleep_seconds=1,
)
async def _process_group(
    cursor: cursor_cls,
    group_name: str,
    loaders: Dataloaders,
    progress: float,
) -> None:
    redshift_groups.insert_group(
        cursor=cursor,
        item=await get_group_item(group_name=group_name),
    )
    redshift_groups.insert_historic_state(
        cursor=cursor,
        group_name=group_name,
        historic_state=await get_group_historic_state_items(
            group_name=group_name
        ),
    )
    unreliable_indicators = await get_group_unreliable_indicators_item(
        group_name=group_name
    )
    if unreliable_indicators:
        redshift_groups.insert_code_languages(
            cursor=cursor,
            unreliable_indicators=unreliable_indicators,
        )
    await group_comments_domain.remove_comments(group_name)
    await groups_domain.remove_all_stakeholders(
        loaders=loaders,
        group_name=group_name,
        modified_by="integrates@fluidattacks.com",
    )
    await groups_model.remove(group_name=group_name)
    LOGGER_CONSOLE.info(
        "Group processed",
        extra={
            "extra": {
                "group_name": group_name,
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
    with redshift_ops.db_cursor() as cursor:
        await collect(
            tuple(
                _process_group(
                    cursor=cursor,
                    group_name=group_name,
                    loaders=loaders,
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
