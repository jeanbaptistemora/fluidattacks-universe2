# Standard library
from typing import (
    NamedTuple,
    Tuple,
)

# Third party libraries
from aioextensions import (
    collect,
    run
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
    TREATMENT,
)

Treatment = NamedTuple('Treatment', [
    ('acceptedUndefined', int),
    ('accepted', int),
    ('inProgress', int),
    ('undefined', int),
])


@alru_cache(maxsize=None, typed=True)
async def get_data_one_group(group: str):
    item = await group_domain.get_attributes(group, ['total_treatment'])

    treatment = item.get('total_treatment', {})

    return Treatment(
        acceptedUndefined=treatment.get('acceptedUndefined', 0),
        accepted=treatment.get('accepted', 0),
        inProgress=treatment.get('inProgress', 0),
        undefined=treatment.get('undefined', 0),
    )


async def get_data_many_groups(groups: Tuple[str]):
    groups_data = await collect(map(get_data_one_group, list(groups)))

    return Treatment(
        acceptedUndefined=sum(
            [group.acceptedUndefined for group in groups_data]
        ),
        accepted=sum([group.accepted for group in groups_data]),
        inProgress=sum([group.inProgress for group in groups_data]),
        undefined=sum([group.undefined for group in groups_data]),
    )


def format_data(data: Treatment):
    translations = {
        'acceptedUndefined': 'Eternally accepted',
        'accepted': 'Temporarily Accepted',
        'inProgress': 'In Progress',
        'undefined': 'Not defined',
    }

    return {
        'data': {
            'columns': [
                [translations[column], getattr(data, column)]
                for column in translations
            ],
            'type': 'pie',
            'colors': {
                'Eternally accepted': TREATMENT.more_passive,
                'Temporarily Accepted': TREATMENT.passive,
                'In Progress': TREATMENT.neutral,
                'Not defined': TREATMENT.more_agressive,
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
            document=format_data(
                data=await get_data_one_group(group),
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
