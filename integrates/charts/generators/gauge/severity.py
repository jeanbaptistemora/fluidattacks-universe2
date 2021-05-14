# Standard library
from typing import (
    Iterable,
    NamedTuple,
)

# Third party libraries
from aioextensions import (
    collect,
    run,
)
from async_lru import alru_cache

# Local libraries
from charts import utils
from charts.colors import RISK
from dataloaders import get_new_context


Severity = NamedTuple('Severity', [
    ('max_open_severity', float),
    ('max_severity_found', float),
])


@alru_cache(maxsize=None, typed=True)
async def generate_one(group: str) -> Severity:
    context = get_new_context()
    group_loader = context.group_all
    group_findings_loader = context.group_findings
    finding_loader = context.finding

    group_findings_data = await group_findings_loader.load(group.lower())
    finding_ids = [finding['finding_id'] for finding in group_findings_data]
    findings = await finding_loader.load_many(finding_ids)

    max_severity_found = 0 if not findings else max(
        finding['severity_score']
        for finding in findings
        if 'current_state' in finding
        and finding['current_state'] != 'DELETED'
    )

    group_data = await group_loader.load(group.lower())
    max_open_severity = group_data['max_open_severity']

    return Severity(
        max_open_severity=max_open_severity,
        max_severity_found=max_severity_found,
    )


async def get_data_many_groups(groups: Iterable[str]) -> Severity:
    groups_data = await collect(map(generate_one, groups))

    return Severity(
        max_open_severity=0 if not groups_data else max(
            [group.max_open_severity for group in groups_data]
        ),
        max_severity_found=0 if not groups_data else max(
            [group.max_severity_found for group in groups_data]
        ),
    )


def format_data(data: Severity) -> dict:
    return {
        'color': {
            'pattern': [RISK.more_passive, RISK.more_agressive],
        },
        'data': {
            'columns': [
                ['Max severity found', data.max_severity_found],
                ['Max open severity', data.max_open_severity],
            ],
            'type': 'gauge',
        },
        'gauge': {
            'label': {
                'format': None,
                'show': True,
            },
            'max': 10,
            'min': 0,
        },
        'gaugeClearFormat': True,
        'legend': {
            'position': 'right',
        },
    }


async def generate_all() -> None:
    async for group in utils.iterate_groups():
        utils.json_dump(
            document=format_data(
                data=await generate_one(group),
            ),
            entity='group',
            subject=group,
        )

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        utils.json_dump(
            document=format_data(
                data=await get_data_many_groups(org_groups),
            ),
            entity='organization',
            subject=org_id,
        )

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
    run(generate_all())
