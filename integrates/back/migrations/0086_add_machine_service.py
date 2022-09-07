# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# /usr/bin/env python3
# -.- coding: utf-8 -.-
# pylint: disable=invalid-name
"""
This migration adds an attribute for the new service in a group's
historic configuration

Execution Time:    2021-05-06 at 15:18:09 UTC-05
Finalization Time: 2021-05-06 at 15:18:20 UTC-05
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
                *historic_config[:-1],
                {
                    **historic_config[-1],
                    "has_skims": historic_config[-1]["has_drills"],
                },
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
