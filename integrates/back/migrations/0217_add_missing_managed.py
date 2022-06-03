# pylint: disable=invalid-name
"""
add managed field to all groups

Execution Time:    2022-05-18 at 03:31:48 UTC
Finalization Time: 2022-05-18 at 03:33:15 UTC
"""

from aioextensions import (
    collect,
    run,
)
from dynamodb.types import (
    Item,
)
from groups.dal import (  # pylint: disable=import-error
    _get_attributes,
    _update,
)
import logging
import logging.config
from organizations.domain import (
    iterate_organizations_groups,
)
from settings import (
    LOGGING,
)
import time

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def process_group(
    *,
    group_name: str,
    progress: float,
) -> None:
    item_to_update: Item = {}
    current_group_item = await _get_attributes(
        group_name=group_name,
        attributes=["historic_configuration"],
    )

    if "managed" in current_group_item["historic_configuration"][-1]:
        return

    item_to_update["historic_configuration"] = [
        *current_group_item["historic_configuration"][:-1],
        {
            **current_group_item["historic_configuration"][-1],
            "managed": True,
        },
    ]
    await _update(
        group_name=group_name,
        data=item_to_update,
    )
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
    group_names = []
    async for _, _, org_group_names in iterate_organizations_groups():
        group_names.extend(org_group_names)
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
                group_name=group_name,
                progress=count / group_names_len,
            )
            for count, group_name in enumerate(set(group_names))
        ),
        workers=2,
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
