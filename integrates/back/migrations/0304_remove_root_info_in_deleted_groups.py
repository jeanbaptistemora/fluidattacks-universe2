# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=invalid-name
"""
From deleted groups, remove unneeded root related items.
The following root related facets won't be archived:
    machine_git_root_execution
    root_environment_secret
    root_environment_url
    root_secret

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
    roots as roots_model,
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


async def _process_root(
    group_name: str,
    root_id: str,
) -> None:
    await roots_model.remove_root_machine_executions(root_id=root_id)
    await roots_model.remove_root_environment_urls(root_id=root_id)
    await roots_model.remove_root_secrets(root_id=root_id)
    LOGGER_CONSOLE.info(
        "Root processed",
        extra={"extra": {"group_name": group_name, "root_id": root_id}},
    )


async def _process_group(
    loaders: Dataloaders,
    group_name: str,
    progress: float,
) -> None:
    roots = await loaders.group_roots.load(group_name)
    await collect(
        tuple(
            _process_root(group_name=group_name, root_id=root.id)
            for root in roots
        ),
        workers=8,
    )
    LOGGER_CONSOLE.info(
        "Group processed",
        extra={
            "extra": {
                "group_name": group_name,
                "len(items)": len(roots),
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
                loaders=loaders,
                group_name=group_name,
                progress=count / len(deleted_group_names),
            )
            for count, group_name in enumerate(deleted_group_names)
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
