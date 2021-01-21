# Standard library
from collections import Counter
from typing import List

# Third party libraries
from aioextensions import (
    collect,
    run,
)
from async_lru import alru_cache
from backend.api.dataloaders.finding import FindingLoader
from backend.api.dataloaders.project import ProjectLoader as GroupLoader
from backend.domain.finding import get_finding_open_age

# Local libraries
from analytics import utils
from analytics.colors import RISK


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(group: str) -> Counter:
    group_data = await GroupLoader().load(group.lower())
    findings = await FindingLoader().load_many(group_data['findings'])

    return Counter({
        f'{finding_id}/{finding["title"]}': await get_finding_open_age(
            finding_id
        )
        for finding, finding_id in zip(findings, group_data['findings'])
    })


async def get_data_many_groups(groups: List[str]) -> Counter:
    groups_data = await collect(map(get_data_one_group, groups))

    return sum(groups_data, Counter())


def format_data(counters: Counter) -> dict:
    data = [
        (title, open_age)
        for title, open_age in counters.most_common()[:10]
        if open_age > 0
    ]

    return dict(
        data=dict(
            columns=[
                ['Open Age (days)'] + [open_age for _, open_age in data],
            ],
            colors={
                'Open Age (days)': RISK.neutral,
            },
            type='bar',
        ),
        legend=dict(
            position='bottom',
        ),
        axis=dict(
            x=dict(
                categories=[
                    title.split('/')[-1].split(' -')[0] for title, _ in data
                ],
                type='category',
                tick=dict(
                    outer=False,
                    rotate=12,
                ),
            ),
            y=dict(
                min=0,
                padding=dict(
                    bottom=0,
                ),
            ),
        ),
        barChartYTickFormat=True,
    )


async def generate_all():
    async for org_id, org_name, _ in utils.iterate_organizations_and_groups():
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            utils.json_dump(
                document=format_data(
                    counters=await get_data_many_groups(groups),
                ),
                entity='portfolio',
                subject=f'{org_id}PORTFOLIO#{portfolio}',
            )


if __name__ == '__main__':
    run(generate_all())
