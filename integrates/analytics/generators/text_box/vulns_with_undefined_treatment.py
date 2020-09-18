# Standard library
import asyncio
from typing import (
    Tuple,
)

# Third party libraries
from aioextensions import (
    collect,
)
from backend.domain import (
    project as group_domain,
)

# Local libraries
from analytics import (
    utils,
)


async def generate_one(group: str) -> int:
    item = await group_domain.get_attributes(group, ['total_treatment'])

    return item.get('total_treatment', {}).get('undefined', 0)


async def get_undefined_count_many_groups(groups: Tuple[str]) -> int:
    groups_undefined_vulns = await collect(map(generate_one, list(groups)))

    return sum(groups_undefined_vulns)


def format_data(undefined_count: int) -> dict:
    return {
        'fontSizeRatio': 0.5,
        'text': undefined_count,
    }


async def generate_all():
    async for group in utils.iterate_groups():
        utils.json_dump(
            document=format_data(
                undefined_count=await generate_one(group),
            ),
            entity='group',
            subject=group,
        )

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        utils.json_dump(
            document=format_data(
                undefined_count=await get_undefined_count_many_groups(
                    org_groups
                ),
            ),
            entity='organization',
            subject=org_id,
        )


if __name__ == '__main__':
    asyncio.run(generate_all())
