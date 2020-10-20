# Standard library
from decimal import (
    Decimal,
)
from statistics import (
    mean,
)
from typing import (
    List,
    NamedTuple,
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
from analytics.colors import (
    RISK,
)

Remediate = NamedTuple('Remediate', [
    ('critical_severity', Decimal),
    ('high_severity', Decimal),
    ('medium_severity', Decimal),
    ('low_severity', Decimal),
])


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(group: str) -> Remediate:
    group_data = await group_domain.get_attributes(group, [
        'mean_remediate_critical_severity',
        'mean_remediate_high_severity',
        'mean_remediate_medium_severity',
        'mean_remediate_low_severity',
    ])

    return Remediate(
        critical_severity=group_data.get(
            'mean_remediate_critical_severity', 0
        ),
        high_severity=group_data.get('mean_remediate_high_severity', 0),
        medium_severity=group_data.get('mean_remediate_medium_severity', 0),
        low_severity=group_data.get('mean_remediate_low_severity', 0),
    )


async def get_data_many_groups(
        groups: List[str]) -> Remediate:
    groups_data = await collect(map(get_data_one_group, groups))

    return Remediate(
        critical_severity=Decimal(mean([
            group.critical_severity for group in groups_data
        ])).quantize(Decimal('0.1')),
        high_severity=Decimal(mean([
            group.high_severity for group in groups_data
        ])).quantize(Decimal('0.1')),
        medium_severity=Decimal(mean([
            group.medium_severity for group in groups_data
        ])).quantize(Decimal('0.1')),
        low_severity=Decimal(mean([
            group.low_severity for group in groups_data
        ])).quantize(Decimal('0.1')),
    )


def format_data(data: Remediate) -> dict:
    translations = {
        'critical_severity': 'Critical Severity',
        'high_severity': 'High Severity',
        'medium_severity': 'Medium Severity',
        'low_severity': 'Low Severity',
    }
    return dict(
        data=dict(
            columns=[
                ['Mean time to remediate'] + [
                    getattr(data, column) for column in translations
                ]
            ],
            colors={
                'Mean time to remediate': RISK.neutral,
            },
            type='bar',
        ),
        axis=dict(
            x=dict(
                categories=[translations[column] for column in translations],
                type='category',
            ),
        ),
    )


async def generate_all():
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
