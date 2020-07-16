# Standard library
import asyncio
from functools import reduce
from typing import (
    cast,
    Dict,
    List
)

# Third party libraries
from backend.api.dataloaders.project import (
    ProjectLoader as GroupLoader,
)
from backend.typing import (
    Project as ProjectType
)

# Local libraries
from analytics import (
    utils,
)


async def generate_one(groups: List[str]):
    group_data = await GroupLoader().load_many(groups)

    def filter_last_week(group: ProjectType, index: int):
        attrs = cast(Dict[str, List[List[Dict[str, int]]]], group['attrs'])
        remediated_over_time = attrs.get('remediated_over_time', [])
        total = 0

        if remediated_over_time:
            item = remediated_over_time[index]
            total = int(item[-1].get('y', 0)) if item else 0

        return total

    found_last_week: int = reduce(
        lambda acc, group: acc + filter_last_week(group, 0), group_data, 0)
    closed_last_week: int = reduce(
        lambda acc, group: acc + filter_last_week(group, 1), group_data, 0)

    open_vulns: int = reduce(
        lambda acc, group:
            acc + int(group['attrs'].get('open_vulnerabilities', 0)),
        group_data, 0)
    closed_vulns: int = reduce(
        lambda acc, group:
            acc + int(group['attrs'].get('closed_vulnerabilities', 0)),
        group_data, 0)

    return {
        'previous': {
            'closed': closed_last_week,
            'open': found_last_week - closed_last_week,
        },
        'current': {
            'closed': closed_vulns,
            'open': open_vulns,
        },
    }


async def generate_all():
    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        utils.json_dump(
            document=await generate_one(org_groups),
            entity='organization',
            subject=org_id,
        )


if __name__ == '__main__':
    asyncio.run(generate_all())
