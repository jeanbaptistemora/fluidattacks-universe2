# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
# type: ignore

# pylint: disable=invalid-name
# create all groups metadata if the group is active
#
# Execution time: Fri Jun 18 13:53:32 -05 2021
# Finalization time: Fri Jun 18 13:55:14 -05 2021

import aioextensions
from contextlib import (
    suppress,
)
from dynamodb.model import (
    update_group_agent_token,
)
from forces.domain import (
    get_token,
)
from groups.domain import (
    get_groups_with_forces,
)


@aioextensions.run_decorator
async def main() -> None:
    groups = await get_groups_with_forces()
    for group in groups:
        print(f"[INFO] processing {group}")
        with suppress(Exception):
            current_token = await get_token(group)
            if current_token:
                await update_group_agent_token(
                    group_name=group,
                    agent_token=current_token,
                )


main()
