# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=invalid-name
"""
Trigger remove_resources on deleted groups, as some of them still have
non_removed/unmasked data on dynamodb.
The origin could be early failures on the remove_resources batch action.

Execution Time:
Finalization Time:
"""

from aioextensions import (
    run,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.groups.enums import (
    GroupStateStatus,
)
from groups import (
    domain as groups_domain,
)
from organizations.domain import (
    get_all_deleted_groups,
)
import time


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    deleted_groups = sorted(await get_all_deleted_groups(loaders))
    print(f"Groups to process: {len(deleted_groups)=}")
    for count, group in enumerate(deleted_groups):
        if group.state.status == GroupStateStatus.DELETED:
            await groups_domain.remove_resources(
                loaders=loaders,
                group_name=group.name,
                user_email="integrates@fluidattacks.com",
            )
            print(
                f"Group processed: {group=}, "
                f"progress: {round(count / len(deleted_groups), 2)}"
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
