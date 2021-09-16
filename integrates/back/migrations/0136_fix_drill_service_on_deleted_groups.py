# pylint: disable=invalid-name
"""
This migration updates active services to false on deleted groups

Execution Time:
Finalization Time:
"""

from aioextensions import (
    collect,
    run,
)
from groups.dal import (
    get_attributes,
    update,
)
import time

# Constants
PROD: bool = False


async def update_group(group_name: str) -> bool:
    historic_config = (
        await get_attributes(group_name, ["historic_configuration"])
    )["historic_configuration"]

    success = False

    if PROD:
        print(f"Working on {group_name} group!")
        success = await update(
            group_name,
            {
                "historic_configuration": [
                    *historic_config[:-1],
                    {
                        **historic_config[-1],
                        "has_drills": False,
                        "has_forces": False,
                        "has_machine": False,
                        "has_skims": False,
                        "has_squad": False,
                    },
                ],
                "project_status": "DELETED",
            },
        )
    else:
        print(f"Working on {group_name} group!")
        print(f"Actual data {historic_config}")
    return success


async def main() -> None:
    groups_to_modify = [
        "abington",
        "apatin",
        "arteaga",
        "carpentersville",
        "gillette",
        "hiachson",
        "morondava",
        "nurch",
        "pimgup",
        "pucsole",
        "rapla",
        "trowpe",
    ]
    success = all(
        await collect(
            tuple(update_group(group_name) for group_name in groups_to_modify)
        )
    )
    print(f"Success: {success}")


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
