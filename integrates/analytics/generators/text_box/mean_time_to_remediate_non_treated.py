# Standard library
from decimal import Decimal
from statistics import mean
from typing import Tuple

# Third party libraries
from aioextensions import (
    collect,
    run,
)
from async_lru import alru_cache
from backend.domain import project as group_domain

# Local libraries
from analytics import utils


@alru_cache(maxsize=None, typed=True)
async def generate_one(group: str) -> Decimal:
    group_data = await group_domain.get_attributes(group, [
        'mean_remediate_non_treated',
    ])

    return group_data.get('mean_remediate_non_treated', 0)


async def get_many_groups(groups: Tuple[str, ...]) -> Decimal:
    groups_data = await collect(map(generate_one, list(groups)))

    return (
        Decimal(mean(groups_data)).quantize(Decimal('0.1'))
        if groups_data else Decimal('Infinity')
    )


def format_data(mean_remediate: Decimal) -> dict:
    return {
        'fontSizeRatio': 0.5,
        'text': mean_remediate,
    }


async def generate_all():
    async for group in utils.iterate_groups():
        utils.json_dump(
            document=format_data(
                mean_remediate=await generate_one(group),
            ),
            entity='group',
            subject=group,
        )

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        utils.json_dump(
            document=format_data(
                mean_remediate=await get_many_groups(org_groups),
            ),
            entity='organization',
            subject=org_id,
        )

    async for org_id, org_name, _ in utils.iterate_organizations_and_groups():
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            utils.json_dump(
                document=format_data(
                    mean_remediate=await get_many_groups(groups),
                ),
                entity='portfolio',
                subject=f'{org_id}PORTFOLIO#{portfolio}',
            )


if __name__ == '__main__':
    run(generate_all())
