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

Status = NamedTuple('Status', [
    ('closed_vulnerabilities', int),
    ('open_vulnerabilities', int),
])


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(group: str) -> Status:
    item = await group_domain.get_attributes(group, [
        'open_vulnerabilities',
        'closed_vulnerabilities',
    ])

    return Status(
        open_vulnerabilities=item.get('open_vulnerabilities', 0),
        closed_vulnerabilities=item.get('closed_vulnerabilities', 0),
    )


async def get_data_many_groups(groups: Tuple[str]) -> Status:
    groups_data = await collect(map(get_data_one_group, list(groups)))

    return Status(
        open_vulnerabilities=sum(
            [group.open_vulnerabilities for group in groups_data]
        ),
        closed_vulnerabilities=sum(
            [group.closed_vulnerabilities for group in groups_data]
        ),
    )


def format_document(data: Status) -> dict:
    return {
        'data': {
            'columns': [
                ['Closed', data.closed_vulnerabilities],
                ['Open', data.open_vulnerabilities],
            ],
            'type': 'pie',
            'colors': {
                'Closed': RISK.more_passive,
                'Open': RISK.more_agressive,
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
            document=format_document(
                data=await get_data_one_group(group),
            ),
            entity='group',
            subject=group,
        )

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        utils.json_dump(
            document=format_document(
                data=await get_data_many_groups(org_groups),
            ),
            entity='organization',
            subject=org_id,
        )


if __name__ == '__main__':
    asyncio.run(generate_all())
