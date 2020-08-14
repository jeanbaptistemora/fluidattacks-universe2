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
    group_data = (await GroupLoader().load(group))

    return {
        'fontSizeRatio': 0.5,
        'text': (
            group_data['attrs'].get('closed_vulnerabilities', 0) +
            group_data['attrs'].get('open_vulnerabilities', 0)
        ),
    }


async def generate_all():
    async for group in utils.iterate_groups():
        utils.json_dump(
            document=await generate_one(group),
            entity='group',
            subject=group,
        )


if __name__ == '__main__':
    asyncio.run(generate_all())
