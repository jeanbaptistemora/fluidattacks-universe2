# pylint: disable=invalid-name
"""
Deletes cloned repos from deleted groups

Execution Time:    2022-06-09 at 18:58:06 UTC-5
Finalization Time: 2022-06-09 at 18:59:15 UTC-5
"""
from aioextensions import (
    collect,
    run,
)
from batch.dal import (
    IntegratesBatchQueue,
    put_action,
)
from batch.enums import (
    Action,
    Product,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.groups.types import (
    Group,
)
from db_model.roots.types import (
    Root,
)
import logging
from organizations.domain import (
    get_all_deleted_groups,
)
import time

# Constants
LOGGER_CONSOLE = logging.getLogger("console")


async def process_group(
    loaders: Dataloaders, group: Group, progress: float
) -> None:
    group_roots: tuple[Root, ...] = await loaders.group_roots.load(group.name)
    success: bool
    if group_roots:
        root_removal = await put_action(
            action=Action.REMOVE_ROOTS,
            entity=group.name,
            subject="machine@fluidattacks.com",
            additional_info=",".join(
                [root.state.nickname for root in group_roots]
            ),
            queue=IntegratesBatchQueue.SMALL,
            product_name=Product.INTEGRATES,
        )
        success = root_removal.success
    else:
        success = True
    LOGGER_CONSOLE.info(
        "Group processed",
        extra={
            "extra": {
                "group_name": group.name,
                "progress": round(progress, 2),
                "success": success,
            }
        },
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    all_deleted_groups: tuple[Group, ...] = await get_all_deleted_groups(
        loaders=loaders
    )

    LOGGER_CONSOLE.info(
        "Deleted groups",
        extra={"extra": {"groups_len": len(all_deleted_groups)}},
    )
    await collect(
        tuple(
            process_group(
                loaders=loaders,
                group=group,
                progress=count / len(all_deleted_groups),
            )
            for count, group in enumerate(all_deleted_groups)
        ),
        workers=4,
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
