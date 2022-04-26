import asyncio
from dataloaders import (
    Dataloaders,
    get_new_context,
)
import json
from organizations import (
    domain as orgs_domain,
)
import sys


async def main() -> None:
    file_path = sys.argv[1]
    loaders: Dataloaders = get_new_context()
    all_active_groups = await orgs_domain.get_all_active_groups_typed(loaders)
    group_names = [
        group.name
        for group in all_active_groups
        if group.state.has_machine or group.state.has_squad
    ]
    with open(file_path, "w") as handler:
        json.dump(group_names, handler)


if __name__ == "__main__":
    asyncio.run(main())
