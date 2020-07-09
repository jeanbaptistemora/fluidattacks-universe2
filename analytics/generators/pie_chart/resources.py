# Standard library
import asyncio

# Third party libraries
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


async def generate_one(group: str):
    group_data = await GroupLoader().load(group)

    repositories = [
        env
        for env in group_data['attrs'].get('repositories', [])
        if 'historic_state' not in env
        or env['historic_state'][-1]['state'].lower() == 'active'
    ]

    environments = [
        env
        for env in group_data['attrs'].get('environments', [])
        if 'historic_state' not in env
        or env['historic_state'][-1]['state'].lower() == 'active'
    ]

    return {
        'data': {
            'columns': [
                ['Repositories', len(repositories)],
                ['Environments', len(environments)],
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
    for group in utils.iterate_groups():
        utils.json_dump(
            document=await generate_one(group),
            entity='group',
            subject=group,
        )


if __name__ == '__main__':
    asyncio.run(generate_all())
