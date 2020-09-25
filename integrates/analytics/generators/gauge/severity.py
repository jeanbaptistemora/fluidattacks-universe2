# Standard library
import asyncio
from typing import (
    NamedTuple,
    Tuple,
)

# Third party libraries
from aioextensions import (
    collect,
)
from async_lru import alru_cache
from backend.api.dataloaders.finding import (
    FindingLoader,
)
from backend.api.dataloaders.project import (
    ProjectLoader as GroupLoader,
)

# Local libraries
from analytics import (
    utils,
)
from analytics.colors import (
    RISK,
)

Severity = NamedTuple('Severity', [
    ('max_open_severity', float),
    ('max_severity_found', float),
])


@alru_cache(maxsize=None, typed=True)
async def generate_one(group: str) -> Severity:
    group_data = await GroupLoader().load(group)

    findings = await FindingLoader().load_many(
        group_data['findings']
    )

    max_severity_found = 0 if not findings else max(
        finding['severity_score']
        for finding in findings
        if 'current_state' in finding
        and finding['current_state'] != 'DELETED'
    )

    max_open_severity = group_data['attrs'].get('max_open_severity', 0)

    return Severity(
        max_open_severity=max_open_severity,
        max_severity_found=max_severity_found,
    )


async def get_data_many_groups(groups: Tuple[str, ...]) -> Severity:
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


async def generate_all():
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


if __name__ == '__main__':
    asyncio.run(generate_all())
