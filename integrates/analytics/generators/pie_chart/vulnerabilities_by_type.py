# Standard library
from collections import Counter
from itertools import chain
from operator import itemgetter
from typing import List

# Third party libraries
from aioextensions import (
    collect,
    run,
)
from async_lru import alru_cache

# Local libraries
from backend.api import get_new_context

from analytics import utils
from analytics.colors import OTHER


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(group: str) -> Counter:
    context = get_new_context()
    group_findings_loader = context.group_findings
    finding_vulns_loader = context.finding_vulns

    group_findings_data = await group_findings_loader.load(group.lower())
    finding_ids = [finding['finding_id'] for finding in group_findings_data]

    vulnerabilities = list(
        chain.from_iterable(
            await finding_vulns_loader.load_many(finding_ids)
        )
    )

    return Counter(filter(None, map(itemgetter('vuln_type'), vulnerabilities)))


async def get_data_many_groups(groups: List[str]) -> Counter:
    groups_data = await collect(map(get_data_one_group, groups))

    return sum(groups_data, Counter())


def format_data(counters: Counter) -> dict:
    translations = {
        'inputs': 'app',
        'lines': 'code',
        'ports': 'infra',
    }

    return {
        'data': {
            'columns': [
                [translations[column], counters[column]]
                for column in translations
            ],
            'type': 'pie',
            'colors': {
                'app': OTHER.more_passive,
                'code': OTHER.neutral,
                'infra': OTHER.more_agressive,
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
