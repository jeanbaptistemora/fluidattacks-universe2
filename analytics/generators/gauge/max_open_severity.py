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
    RISK,
)


async def generate_one(group: str):
    group_data = (await GroupLoader().load(group))

    return {
        'color': {
            'pattern': [RISK.more_agressive],
        },
        'data': {
            'columns': [
                ['CVSS v3', group_data['attrs'].get('max_open_severity', 0)]
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
        'legend': {
            'position': 'bottom',
        },
    }


async def generate_all():
    for group in utils.iterate_groups():
        data = await generate_one(group)
        utils.json_dump(f'group-{group}.json', data)


if __name__ == '__main__':
    asyncio.run(generate_all())
