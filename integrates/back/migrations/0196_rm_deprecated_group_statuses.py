# pylint: disable=invalid-name
"""
In the context of migrating groups to the single table, remove unwanted
statuses SUSPENDED and FINISHED. These are deprecated and only ACTIVE and
DELETED will remain.

This will ease typing and usage of new dataloaders/resolvers.

Execution Time:     2022-02-24 at 21:39:16 UTC
Finalization Time:  2022-02-24 at 21:46:12 UTC
"""

from aioextensions import (
    collect,
    run,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from custom_exceptions import (
    UnavailabilityError as CustomUnavailabilityError,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from decorators import (
    retry_on_exceptions,
)
from dynamodb.exceptions import (
    UnavailabilityError,
)
from groups import (
    dal as groups_dal,
    domain as groups_domain,
)
import logging
import logging.config
from organizations import (
    domain as orgs_domain,
)
from settings import (
    LOGGING,
)
import time
from typing import (
    Any,
    Dict,
    List,
)

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


@retry_on_exceptions(
    exceptions=(
        CustomUnavailabilityError,
        UnavailabilityError,
    ),
    sleep_seconds=10,
)
async def process_group(
    *,
    loaders: Dataloaders,
    group_name: str,
    progress: float,
) -> None:
    group_data = await groups_dal.get_attributes(
        group_name, ["historic_deletion"]
    )
    historic_deletion = group_data.get("historic_deletion", [{}])
    user_deletion = historic_deletion[-1].get("user", "jmesa@fluidattacks.com")
    organization_id = await orgs_domain.get_id_for_group(group_name)

    all_resources_removed = await groups_domain.remove_resources(
        loaders, group_name, user_deletion
    )
    are_users_removed = await groups_domain.remove_all_users(
        loaders, group_name
    )
    try:
        is_removed_from_org = await orgs_domain.remove_group(
            group_name, organization_id
        )
    except CustomUnavailabilityError:
        # This group has no organization assigned
        is_removed_from_org = True
    success = [
        are_users_removed,
        all_resources_removed,
        is_removed_from_org,
    ]

    if all(success):
        new_data: Dict[str, Any] = {
            "group_status": "DELETED",
            "project_status": "DELETED",
        }
        is_updated = await groups_domain.update(group_name, new_data)
        success.append(is_updated)

    LOGGER_CONSOLE.info(
        "Group processed",
        extra={
            "extra": {
                "group_name": group_name,
                "success": success,
                "progress": round(progress, 2),
            }
        },
    )


async def get_groups() -> List[str]:
    filtering_exp = Attr("project_status").eq("SUSPENDED") | Attr(
        "project_status"
    ).eq("FINISHED")
    return sorted(
        [
            group["project_name"]
            for group in await groups_dal.get_all(filtering_exp=filtering_exp)
        ]
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    group_names = await get_groups()
    group_names_len = len(group_names)
    LOGGER_CONSOLE.info(
        "All groups",
        extra={
            "extra": {
                "group_names_len": group_names_len,
            }
        },
    )
    await collect(
        tuple(
            process_group(
                loaders=loaders,
                group_name=group_name,
                progress=count / group_names_len,
            )
            for count, group_name in enumerate(group_names)
        ),
        workers=8,
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
