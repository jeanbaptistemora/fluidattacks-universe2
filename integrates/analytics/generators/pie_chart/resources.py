# Standard library
import asyncio
from typing import (
    List,
    NamedTuple,
    Tuple,
)

# Third party libraries
from aioextensions import (
    collect,
)
from async_lru import (
    alru_cache,
)
from backend.api.dataloaders.project import (
    ProjectLoader as GroupLoader,
)

# Local libraries
from analytics import (
    utils,
)
from analytics.colors import (
    OTHER,
)

Resources = NamedTuple('Resources', [
    ('environments', List[str]),
    ('repositories', List[str]),
])


@alru_cache(maxsize=None, typed=True)
async def generate_one(group: str):
    group_data = await GroupLoader().load(group)

    repositories = [
        f'{env.get("urlRepo", "").lower()}+{env.get("branch", "").lower()}'
        for env in group_data['attrs'].get('repositories', [])
        if 'historic_state' not in env
        or env['historic_state'][-1]['state'].lower() == 'active'
    ]

    environments = [
        str(env.get('urlEnv', '').lower())
        for env in group_data['attrs'].get('environments', [])
        if 'historic_state' not in env
        or env['historic_state'][-1]['state'].lower() == 'active'
    ]

    return Resources(
        environments=environments,
        repositories=repositories,
    )


async def get_data_many_groups(groups: Tuple[str]) -> Resources:
    groups_data = await collect(map(generate_one, list(groups)))

    return Resources(
        environments=list(
            set(env for group in groups_data for env in group.environments)
        ),
        repositories=list(
            set(repo for group in groups_data for repo in group.repositories)
        ),
    )


def format_data(data: Resources) -> dict:
    return {
        'data': {
            'columns': [
                ['Repositories', len(data.repositories)],
                ['Environments', len(data.environments)],
            ],
            'type': 'pie',
            'colors': {
                'Repositories': OTHER.more_passive,
                'Environments': OTHER.more_agressive,
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
