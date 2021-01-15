# Standard library
from collections import Counter
from itertools import chain
from typing import List

# Third party libraries
from aioextensions import (
    collect,
    run,
)
from async_lru import alru_cache
from backend.api.dataloaders.project import ProjectLoader as GroupLoader
from backend.api.dataloaders.finding_vulns import FindingVulnsLoader

# Local libraries
from analytics import utils
from analytics.colors import RISK


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(group: str) -> Counter:
    group_data = await GroupLoader().load(group.lower())
    vulnerabilities = list(
        chain.from_iterable(
            await FindingVulnsLoader().load_many(group_data['findings'])
        )
    )

    return Counter([
        vuln['historic_treatment'][-1]['user'] for vuln in vulnerabilities
        if vuln['historic_treatment'][-1]['treatment'] == 'ACCEPTED'
        and vuln['historic_state'][-1]['state'] == 'open'
    ])


async def get_data_many_groups(groups: List[str]) -> Counter:
    groups_data = await collect(map(get_data_one_group, groups))

    return sum(groups_data, Counter())


def format_data(counters: Counter) -> dict:
    data = counters.most_common()[:10]

    return dict(
        data=dict(
            columns=[
                ['# Accepted vulnerabilities'] + [
                    accepted_vulns for _, accepted_vulns in data
                ],
            ],
            colors={
                '# Accepted vulnerabilities': RISK.neutral,
            },
            type='bar',
        ),
        legend=dict(
            position='bottom',
        ),
        axis=dict(
            x=dict(
                categories=[user for user, _ in data],
                type='category',
                tick=dict(
                    rotate=12,
                    multiline=False,
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
