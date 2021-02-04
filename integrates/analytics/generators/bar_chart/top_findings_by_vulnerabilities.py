# Standard library
from collections import Counter
from typing import List

# Third party libraries
from aioextensions import (
    collect,
    run,
)
from async_lru import alru_cache
from backend.api import get_new_context

# Local libraries
from analytics import utils
from analytics.colors import RISK


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(group: str) -> Counter:
    context = get_new_context()
    group_loader = context.project
    finding_loader = context.finding
    finding_vulns_loader = context.finding_vulns

    group_data = await group_loader.load(group)
    findings = await finding_loader.load_many(group_data['findings'])
    finding_vulns = await finding_vulns_loader.load_many(
        group_data['findings']
    )

    return Counter([
        f'{finding["finding_id"]}/{finding["title"]}'
        for finding, vulnerabilities in zip(findings, finding_vulns)
        for vulnerability in vulnerabilities
        if vulnerability['current_state'] == 'open'
    ])


async def get_data_many_groups(groups: List[str]) -> Counter:
    groups_data = await collect(map(get_data_one_group, groups))

    return sum(groups_data, Counter())


def format_data(counters: Counter) -> dict:
    data = counters.most_common()[:10]

    return dict(
        data=dict(
            columns=[
                ['# Open Vulnerabilities'] + [value for _, value in data],
            ],
            colors={
                '# Open Vulnerabilities': RISK.neutral,
            },
            type='bar',
        ),
        legend=dict(
            position='bottom',
        ),
        axis=dict(
            x=dict(
                categories=[
                    key.split('/')[-1].split(' -')[0] for key, _ in data
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
    async for group in utils.iterate_groups():
        utils.json_dump(
            document=format_data(counters=await get_data_one_group(group)),
            entity='group',
            subject=group,
        )

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        utils.json_dump(
            document=format_data(
                counters=await get_data_many_groups(list(org_groups)),
            ),
            entity='organization',
            subject=org_id,
        )

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
