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


async def generate_one(group: str):
    group_data = await GroupLoader().load(group)

    has_forces = \
        group_data['attrs']['historic_configuration'][-1]['has_forces']

    return {
        'text': 'Active' if has_forces else 'Inactive',
    }


async def generate_all():
    for group in utils.iterate_groups():
        data = await generate_one(group)
        utils.json_dump(f'group-{group}.json', data)


if __name__ == '__main__':
    asyncio.run(generate_all())
