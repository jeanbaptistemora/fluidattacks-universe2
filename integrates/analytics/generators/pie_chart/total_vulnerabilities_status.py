# Standard library
from typing import (
    List,
)

# Third party libraries
from aioextensions import (
    collect,
    run,
)
from async_lru import alru_cache
from backend.domain import (
    project as group_domain,
)

# Local libraries
from analytics import (
    utils,
)
from analytics.generators.pie_chart.utils import (
    format_data,
    PortfoliosGroupsInfo,
    slice_groups,
)


@alru_cache(maxsize=None, typed=True)
async def get_data_group(group: str) -> PortfoliosGroupsInfo:
    item = await group_domain.get_attributes(group, [
        'open_vulnerabilities',
        'closed_vulnerabilities',
    ])

    return PortfoliosGroupsInfo(
        group_name=group.lower(),
        value=item.get('open_vulnerabilities', 0) +
        item.get('closed_vulnerabilities', 0)
    )


async def get_data_groups(groups: List[str]) -> List[PortfoliosGroupsInfo]:
    groups_data = await collect(map(get_data_group, groups))
    total_vulnerabilities = sum(
        [group.value for group in groups_data]
    )

    return slice_groups(groups_data, total_vulnerabilities)


async def generate_all():
    async for org_id, org_name, _ in utils.iterate_organizations_and_groups():
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            utils.json_dump(
                document=format_data(
                    groups_data=await get_data_groups(groups),
                ),
                entity='portfolio',
                subject=f'{org_id}PORTFOLIO#{portfolio}',
            )


if __name__ == '__main__':
    run(generate_all())
