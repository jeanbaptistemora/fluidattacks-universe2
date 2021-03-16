# Standard library
from typing import Tuple

# Third party libraries
from aioextensions import (
    collect,
    run,
)
from async_lru import alru_cache

# Local libraries
from backend.api import get_new_context
from charts import utils


@alru_cache(maxsize=None, typed=True)
async def generate_one(group: str) -> int:
    context = get_new_context()
    group_loader = context.group_all
    group_data = (await group_loader.load(group))

    return (
        group_data['closed_vulnerabilities'] +
        group_data['open_vulnerabilities']
    )


async def get_vulns_count_many_groups(groups: Tuple[str]) -> int:
    groups_vulns = await collect(map(generate_one, list(groups)))

    return sum(groups_vulns)


def format_data(vulns_count: int) -> dict:
    return {
        'fontSizeRatio': 0.5,
        'text': vulns_count,
    }


async def generate_all():
    async for group in utils.iterate_groups():
        utils.json_dump(
            document=format_data(
                vulns_count=await generate_one(group),
            ),
            entity='group',
            subject=group,
        )

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        utils.json_dump(
            document=format_data(
                vulns_count=await get_vulns_count_many_groups(org_groups),
            ),
            entity='organization',
            subject=org_id,
        )

    async for org_id, org_name, _ in utils.iterate_organizations_and_groups():
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            utils.json_dump(
                document=format_data(
                    vulns_count=await get_vulns_count_many_groups(groups),
                ),
                entity='portfolio',
                subject=f'{org_id}PORTFOLIO#{portfolio}',
            )


if __name__ == '__main__':
    run(generate_all())
