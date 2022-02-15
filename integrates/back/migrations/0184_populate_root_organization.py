# pylint: disable=invalid-name
"""
This migration populates the attributes to be used as index keys for the new
get_organization_roots access pattern.

Execution Time:
Finalization Time:
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
from db_model.roots.constants import (
    ORG_INDEX_METADATA,
)
from db_model.roots.types import (
    RootItem,
)
from dynamodb import (
    keys,
    operations,
)
from groups import (
    dal as groups_dal,
)
import logging
from settings import (
    LOGGING,
)
import time
from typing import (
    List,
)

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


index = TABLE.indexes["inverted_index"]
key_structure = index.primary_key


async def process_root(organization_name: str, root: RootItem) -> None:
    root_key = keys.build_key(
        facet=TABLE.facets["git_root_metadata"],
        values={"name": root.group_name, "uuid": root.id},
    )

    if not root.organization_name:
        gsi_2_key = keys.build_key(
            facet=ORG_INDEX_METADATA,
            values={"name": organization_name, "uuid": root.id},
        )

        await operations.update_item(
            key=root_key,
            item={"pk_2": gsi_2_key.partition_key, "sk_2": gsi_2_key.sort_key},
            table=TABLE,
        )


async def process_group(
    loaders: Dataloaders, group_name: str, progress: float
) -> None:
    group = await loaders.group.load(group_name)
    organization = await loaders.organization.load(group["organization"])
    organization_name = organization["name"]
    roots = await loaders.group_roots.load(group_name)

    await collect(
        tuple(process_root(organization_name, root) for root in roots),
        workers=10,
    )

    LOGGER_CONSOLE.info(
        "Group processed",
        extra={
            "extra": {
                "group_name": group_name,
                "roots": len(roots),
                "progress": str(progress),
            }
        },
    )


async def get_group_names() -> List[str]:
    return sorted(
        group["project_name"] for group in await groups_dal.get_all()
    )


async def main() -> None:
    groups = await get_group_names()
    loaders = get_new_context()

    await collect(
        tuple(
            process_group(loaders, group_name, count / len(groups))
            for count, group_name in enumerate(groups)
        ),
        workers=10,
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
