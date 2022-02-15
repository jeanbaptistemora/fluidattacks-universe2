# pylint: disable=invalid-name
"""
This migration populates the last status update of a root as a precalculated
attribute.

Execution Time: 2022-02-15 at 17:32:42 UTC
Finalization Time: 2022-02-15 at 17:37:02 UTC
"""

from aioextensions import (
    collect,
    run,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.roots.types import (
    RootItem,
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
from unreliable_indicators.enums import (
    EntityAttr,
)
from unreliable_indicators.operations import (
    update_root_unreliable_indicators,
)

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


async def process_root(loaders: Dataloaders, root: RootItem) -> None:
    await update_root_unreliable_indicators(
        loaders, (root.group_name, root.id), {EntityAttr.last_status_update}
    )


async def process_group(
    loaders: Dataloaders, group_name: str, progress: float
) -> None:
    roots = await loaders.group_roots.load(group_name)

    await collect(
        tuple(process_root(loaders, root) for root in roots),
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
