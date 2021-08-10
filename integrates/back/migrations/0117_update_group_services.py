# pylint: disable=invalid-name
"""
This migration updates the machine service ensuring it is only enabled in
groups with service type white

Execution Time:
Finalization Time:
"""

from aioextensions import (
    collect,
    run,
)
from groups.dal import (
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
                    "has_skims": item["service"] == "WHITE"
                    and item["has_skims"],
                    "has_machine": item["service"] == "WHITE"
                    and item["has_skims"],
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
