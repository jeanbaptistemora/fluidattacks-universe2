# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# /usr/bin/env python3
# pylint: disable=invalid-name
"""
This migration removes all erased groups from the portfolios

Execution Time:    2021-06-01 at 13:18:00 UTC-05
Finalization Time: 2021-06-01 at 13:20:00 UTC-05
"""


from aioextensions import (
    run,
)
from dataloaders import (
    GroupLoader,
)
from dynamodb.operations_legacy import (
    scan,
)
from tags import (
    domain as tags_domain,
)
from tags.dal import (  # pylint: disable=import-error
    TABLE_NAME as TAGS_TABLE,
)
import time


async def main() -> None:
    scan_attrs = {"ProjectionExpression": "organization,projects,tag"}
    all_tags = await scan(TAGS_TABLE, scan_attrs)
    for tag in all_tags:
        groups = await GroupLoader().load_many(tag["projects"])
        active_groups = [
            group["name"]
            for group in groups
            if group["project_status"] == "ACTIVE"
        ]
        if active_groups:
            await tags_domain.update_legacy(active_groups)
            print(
                f"Portfolio {tag['tag']} was updated with groups "
                f"{active_groups}"
            )
        else:
            await tags_domain.remove(tag["organization"], tag["tag"])
            print(f"Portfolio {tag['tag']} was deleted")


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
