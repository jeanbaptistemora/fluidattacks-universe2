# Standard library
from decimal import (
    Decimal,
)
from typing import (
    Tuple,
)

# Third party libraries
from aioextensions import (
    collect,
    run,
)
from async_lru import (
    alru_cache,
)

# Local libraries
from backend.api import get_new_context

from analytics import (
    utils,
)


@alru_cache(maxsize=None, typed=True)
async def generate_one(group: str) -> Decimal:
    context = get_new_context()
    group_loader = context.project
    group_data = await group_loader.load(group)

    return group_data['attrs'].get('last_closing_date', 0)


async def get_many_groups(groups: Tuple[str]) -> Decimal:
    groups_data = await collect(map(generate_one, list(groups)))

    return min(groups_data) if groups_data else Decimal('Infinity')


def format_data(last_closing_date: Decimal) -> dict:
    return {
        'fontSizeRatio': 0.5,
        'text': last_closing_date
    }


async def generate_all():
    async for group in utils.iterate_groups():
        utils.json_dump(
            document=format_data(
                last_closing_date=await generate_one(group)
            ),
            entity='group',
            subject=group,
        )

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        utils.json_dump(
            document=format_data(
                last_closing_date=await get_many_groups(
                    org_groups
                ),
            ),
            entity='organization',
            subject=org_id,
        )

    async for org_id, org_name, _ in (
        utils.iterate_organizations_and_groups()
    ):
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            utils.json_dump(
                document=format_data(
                    last_closing_date=await get_many_groups(groups),
                ),
                entity='portfolio',
                subject=f'{org_id}PORTFOLIO#{portfolio}',
            )


if __name__ == '__main__':
    run(generate_all())
