# pylint: disable=invalid-name
"""
Populate items for facet group_id. This items will keep group names as unique
identifiers, even after the group metadata removal from dynamodb.

Execution Time:    2022-11-09 at 19:00:05 UTC
Finalization Time: 2022-11-09 at 19:01:20 UTC
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
    TABLE,
)
from dynamodb import (
    keys,
    operations,
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

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def _process_group(
    group_name: str,
    progress: float,
) -> None:
    key_structure = TABLE.primary_key
    facet = TABLE.facets["group_id"]
    id_key = keys.build_key(
        facet=facet,
        values={"name": group_name},
    )
    id_item = {
        key_structure.partition_key: id_key.partition_key,
        key_structure.sort_key: id_key.sort_key,
    }
    await operations.put_item(
        facet=facet,
        item=id_item,
        table=TABLE,
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
    loaders: Dataloaders = get_new_context()
    active_group_names = [
        group.name
        for group in await orgs_domain.get_all_active_groups(loaders)
    ]
    deleted_group_names = [
        group.name
        for group in await orgs_domain.get_all_deleted_groups(loaders)
    ]
    all_group_names = sorted(active_group_names + deleted_group_names)
    LOGGER_CONSOLE.info(
        "All groups",
        extra={"extra": {"groups_len": len(all_group_names)}},
    )

    await collect(
        tuple(
            _process_group(
                group_name=group_name,
                progress=count / len(all_group_names),
            )
            for count, group_name in enumerate(all_group_names)
        ),
        workers=16,
    )


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
