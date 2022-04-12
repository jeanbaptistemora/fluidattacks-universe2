import asyncio
from groups import (
    domain as groups_domain,
)
import json
from newutils.groups import (
    format_group,
)
import sys


async def main() -> None:
    file_path = sys.argv[1]
    groups_items = await groups_domain.get_many_groups(
        await groups_domain.get_active_groups()
    )
    groups = tuple(
        format_group(item=group, organization_name="")
        for group in groups_items
    )
    groups = [
        group.name
        for group in groups
        if group.state.has_machine or group.state.has_machine
    ]
    with open(file_path, "w") as handler:
        json.dump(groups, handler)


if __name__ == "__main__":
    asyncio.run(main())
