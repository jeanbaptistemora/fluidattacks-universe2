# Standard library
import asyncio
from typing import (
    List,
    NamedTuple,
)

# Third party libraries
from aioextensions import collect
from async_lru import alru_cache
from backend.domain import (
    project as group_domain,
)

# Local libraries
from analytics import (
    utils,
)
from analytics.colors import (
    TREATMENT,
    RISK,
)

Treatment = NamedTuple('Status', [
    ('accepted', int),
    ('accepted_undefined', int),
    ('group_name', str),
    ('closed_vulnerabilities', int),
    ('open_vulnerabilities', int),
    ('remaining_open_vulnerabilities', int),
])


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(group: str) -> Treatment:
    item = await group_domain.get_attributes(group, [
        'open_vulnerabilities',
        'closed_vulnerabilities',
        'total_treatment',
    ])
    treatment = item.get('total_treatment', {})
    open_vulnerabilities: int = item.get('open_vulnerabilities', 0)
    accepted_vulnerabilities: int = (
        treatment.get('acceptedUndefined', 0) + treatment.get('accepted', 0)
    )

    return Treatment(
        group_name=group.lower(),
        accepted=treatment.get('accepted', 0),
        accepted_undefined=treatment.get('acceptedUndefined', 0),
        remaining_open_vulnerabilities=(
            open_vulnerabilities - accepted_vulnerabilities
        ),
        open_vulnerabilities=open_vulnerabilities,
        closed_vulnerabilities=item.get('closed_vulnerabilities', 0),
    )


async def get_data_many_groups(groups: List[str]) -> List[Treatment]:
    groups_data = await collect(map(get_data_one_group, groups))

    return sorted(
        groups_data,
        key=lambda x: (
            x.closed_vulnerabilities
            / (x.closed_vulnerabilities + x.open_vulnerabilities)
            if (x.closed_vulnerabilities + x.open_vulnerabilities) > 0
            else 0
        )
    )


def format_data(data: List[Treatment]) -> dict:
    return dict(
        data=dict(
            columns=[
                ['Closed'] + [group.closed_vulnerabilities for group in data],
                ['Temporarily Accepted'] + [group.accepted for group in data],
                ['Eternally accepted'] + [
                    group.accepted_undefined for group in data
                ],
                ['Open'] + [
                    group.remaining_open_vulnerabilities for group in data
                ],
            ],
            colors={
                'Closed': RISK.more_passive,
                'Temporarily Accepted': TREATMENT.passive,
                'Eternally accepted': TREATMENT.more_passive,
                'Open': RISK.more_agressive,
            },
            type='bar',
            groups=[
                [
                    'Closed',
                    'Temporarily Accepted',
                    'Eternally accepted',
                    'Open'
                ],
            ],
            order=None,
            stack=dict(
                normalize=True,
            )
        ),
        legend=dict(
            position='bottom',
        ),
        axis=dict(
            x=dict(
                categories=[group.group_name for group in data],
                type='category',
                tick=dict(
                    rotate=utils.TICK_ROTATION,
                    multiline=False
                )
            ),
        ),
    )


async def generate_all():
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
    asyncio.run(generate_all())
