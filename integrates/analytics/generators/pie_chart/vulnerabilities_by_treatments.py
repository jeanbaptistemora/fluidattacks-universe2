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
from backend.typing import Vulnerability

# Local libraries
from analytics import utils
from analytics.colors import OTHER
from analytics.generators.pie_chart.utils import MAX_GROUPS_DISPLAYED


def get_treatment_changes(vuln: Vulnerability) -> int:
    return (
        len(vuln['historic_treatment']) -
        (1 if vuln['historic_treatment'][0]['treatment'] == "NEW" else 0)
    )


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(group: str) -> Counter:
    group_data = await GroupLoader().load(group.lower())
    vulnerabilities = list(
        chain.from_iterable(
            await FindingVulnsLoader().load_many(group_data['findings'])
        )
    )

    return Counter(filter(None, map(get_treatment_changes, vulnerabilities)))


async def get_data_many_groups(groups: List[str]) -> Counter:
    groups_data = await collect(map(get_data_one_group, groups))

    return sum(groups_data, Counter())


def format_data(counters: Counter) -> dict:
    data = counters.most_common()[:MAX_GROUPS_DISPLAYED]

    return {
        'data': {
            'columns': [
                [str(treatment_change), value]
                for treatment_change, value in data
            ],
            'type': 'pie',
            'colors': {
                str(treatment_change[0]): column
                for treatment_change, column in zip(data, OTHER)
            },
        },
        'legend': {
            'position': 'right',
        },
        'pie': {
            'label': {
                'show': True,
            },
        },
    }


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
