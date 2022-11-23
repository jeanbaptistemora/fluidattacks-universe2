# pylint: disable=invalid-name
"""
This migration aims to add the free tier attribute to
all groups' historic_configuration

Execution Time:    2021-12-24 at 00:13:12 UTC
Finalization Time: 2021-12-24 at 00:14:29 UTC
"""

from aioextensions import (
    collect,
    run,
)
from groups import (
    dal,
)
import json
import os
import time
from typing import (
    Any,
)

STAGE = os.environ.get("STAGE", "DEV")


async def add_tier(group: Any) -> None:
    name = group["project_name"]
    historic_config = group.get("historic_configuration", [{}])
    data = {
        "historic_configuration": [
            *historic_config[:-1],
            {
                **historic_config[-1],
                "tier": "free",
            },
        ]
    }
    if STAGE == "PROD":
        print(f"Updating: {name}")
        await dal.update(name, data)
    else:
        print(json.dumps(data, indent=2))


async def main() -> None:
    groups = await dal.get_all(data_attr="project_name,historic_configuration")
    await collect(add_tier(group) for group in groups)


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:     %Y-%m-%d at %H:%M:%S %Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time:  %Y-%m-%d at %H:%M:%S %Z"
    )
    print(f"{execution_time}\n{finalization_time}")
