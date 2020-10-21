# Standard library

# Third party libraries
from aioextensions import run
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
        'fontSizeRatio': 0.5,
        'text': 'Active' if has_forces else 'Inactive',
    }


async def generate_all():
    async for group in utils.iterate_groups():
        utils.json_dump(
            document=await generate_one(group),
            entity='group',
            subject=group,
        )


if __name__ == '__main__':
    run(generate_all())
