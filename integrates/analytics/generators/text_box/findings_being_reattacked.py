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
    return await group_domain.get_pending_closing_check(group)


async def get_many_groups(groups: Tuple[str]) -> int:
    groups_data = await collect(map(generate_one, list(groups)))

    return sum(groups_data)


def format_data(findings_reattack: int) -> dict:
    return {
        'fontSizeRatio': 0.5,
        'text': findings_reattack,
    }


async def generate_all():
    async for group in utils.iterate_groups():
        utils.json_dump(
            document=format_data(findings_reattack=await generate_one(group)),
            entity='group',
            subject=group,
        )

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        utils.json_dump(
            document=format_data(
                findings_reattack=await get_many_groups(
                    org_groups
                ),
            ),
            entity='organization',
            subject=org_id,
        )


if __name__ == '__main__':
    asyncio.run(generate_all())
