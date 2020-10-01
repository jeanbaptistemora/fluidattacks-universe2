# Standard library
import asyncio
from operator import attrgetter
from typing import (
    List,
)

# Third party libraries
from aioextensions import (
    collect,
)
from async_lru import alru_cache
from backend.domain import (
    project as group_domain,
)

# Local libraries
from analytics.generators.pie_chart.utils import (
    PortfoliosGroupsInfo,
)
from analytics import (
    utils,
)
from analytics.colors import (
    RISK,
)


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(group: str) -> PortfoliosGroupsInfo:
    open_findings = await group_domain.get_open_finding(group.lower())

    return PortfoliosGroupsInfo(
        group_name=group.lower(),
        value=open_findings,
    )


async def get_data_many_groups(
        groups: List[str]) -> List[PortfoliosGroupsInfo]:
    groups_data = await collect(map(get_data_one_group, groups))

    return sorted(groups_data, key=attrgetter('value'), reverse=True)


def format_data(data: List[PortfoliosGroupsInfo]) -> dict:
    return dict(
        data=dict(
            columns=[
                ['Open Findings'] + [group.value for group in data],
            ],
            colors={
                'Open Findings': RISK.neutral,
            },
            type='bar',
        ),
        legend=dict(
            position='bottom',
        ),
        axis=dict(
            x=dict(
                categories=[group.group_name for group in data],
                type='category',
                tick=dict(
                    rotate=utils.TICK_ROTATION,
                    multiline=False,
                ),
            ),
        ),
    )


async def generate_all():
    async for org_id, org_name, _ in (
        utils.iterate_organizations_and_groups()
    ):
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            utils.json_dump(
                document=format_data(
                    data=await get_data_many_groups(groups),
                ),
                entity='portfolio',
                subject=f'{org_id}PORTFOLIO#{portfolio}',
            )


if __name__ == '__main__':
    asyncio.run(generate_all())
