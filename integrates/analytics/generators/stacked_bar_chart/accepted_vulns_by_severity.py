# Standard library
from collections import Counter
from typing import List

# Third party libraries
from aioextensions import (
    collect,
    run,
)
from async_lru import alru_cache
from backend.api.dataloaders.project import ProjectLoader as GroupLoader
from backend.api.dataloaders.finding import FindingLoader
from backend.api.dataloaders.finding_vulns import FindingVulnsLoader

# Local libraries
from analytics import utils
from analytics.colors import (
    RISK,
    TREATMENT,
)


def get_severity_level(severity: float) -> str:
    if severity <= 3.9:
        return 'low_severity'
    if 4 <= severity <= 6.9:
        return 'medium_severity'
    if 7 <= severity <= 8.9:
        return 'high_severity'

    return 'critical_severity'


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(group: str) -> Counter:
    group_data = await GroupLoader().load(group.lower())
    findings = await FindingLoader().load_many(group_data['findings'])
    finding_vulns = await FindingVulnsLoader().load_many(
        group_data['findings']
    )
    severity_counter = Counter()
    for finding, vulns in zip(findings, finding_vulns):
        severity = get_severity_level(float(finding['severity_score']))
        for vuln in vulns:
            if vuln['current_state'] == 'open':
                severity_counter.update([f'{severity}_open'])
                if vuln['historic_treatment'][-1]['treatment'] in {
                    'ACCEPTED', 'ACCEPTED_UNDEFINED'
                }:
                    severity_counter.update([severity])

    return severity_counter


async def get_data_many_groups(groups: List[str]) -> Counter:
    groups_data = await collect(map(get_data_one_group, groups))

    return sum(groups_data, Counter())


def format_data(data: Counter) -> dict:
    translations = {
        'critical_severity': 'Critical Severity',
        'high_severity': 'High Severity',
        'medium_severity': 'Medium Severity',
        'low_severity': 'Low Severity',
    }

    return dict(
        data=dict(
            columns=[
                ['# Accepted Vulnerabilities'] + [
                    data[column] for column in translations
                ],
                ['# Open Vulnerabilities'] + [
                    data[f'{column}_open'] - data[column]
                    for column in translations
                ],
            ],
            colors={
                '# Accepted Vulnerabilities': TREATMENT.passive,
                '# Open Vulnerabilities': RISK.more_agressive,
            },
            type='bar',
            groups=[
                ['# Accepted Vulnerabilities', '# Open Vulnerabilities'],
            ],
            order=None,
            stack=dict(
                normalize=True,
            )
        ),
        legend=dict(
            position='bottom',
        ),
        grid=dict(
            y=dict(
                show=True,
            ),
        ),
        axis=dict(
            x=dict(
                categories=[translations[column] for column in translations],
                type='category',
                tick=dict(
                    multiline=False
                )
            ),
        ),
    )


async def generate_all():
    async for group in utils.iterate_groups():
        utils.json_dump(
            document=format_data(data=await get_data_one_group(group)),
            entity='group',
            subject=group,
        )

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        utils.json_dump(
            document=format_data(
                data=await get_data_many_groups(list(org_groups)),
            ),
            entity='organization',
            subject=org_id,
        )

    async for org_id, org_name, _ in (
        utils.iterate_organizations_and_groups()
    ):
        for portfolio, groups in await utils.get_portfolios_groups(org_name):
            if groups:
                utils.json_dump(
                    document=format_data(
                        data=await get_data_many_groups(groups),
                    ),
                    entity='portfolio',
                    subject=f'{org_id}PORTFOLIO#{portfolio}',
                )


if __name__ == '__main__':
    run(generate_all())
