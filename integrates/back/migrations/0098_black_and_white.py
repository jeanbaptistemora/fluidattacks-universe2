# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=invalid-name
"""
This migration adds a service type attribute to groups.
white for continuous and black for oneshot

Execution Time:    2021-07-12 at 16:09:31 UTC-05
Finalization Time: 2021-07-12 at 16:09:44 UTC-05
"""

from aioextensions import (
    collect,
    run,
)
from groups.dal import (  # pylint: disable=import-error
    get_active_groups,
    get_attributes,
    update,
)
import time


async def update_group(group_name: str) -> None:
    historic_config = (
        await get_attributes(group_name, ["historic_configuration"])
    )["historic_configuration"]

    await update(
        group_name,
        {
            "historic_configuration": [
                {
                    **item,
                    "service": "WHITE"
                    if item["type"].lower() == "continuous"
                    else "BLACK",
                }
                for item in historic_config
            ]
        },
    )


async def main() -> None:
    groups = await get_active_groups()
    await collect(tuple(update_group(group_name) for group_name in groups))


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
