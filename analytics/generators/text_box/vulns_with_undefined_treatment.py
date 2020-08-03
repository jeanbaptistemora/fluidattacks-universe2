# Standard library
import asyncio

# Third party libraries
from backend.domain import (
    project as group_domain,
)

# Local libraries
from analytics import (
    utils,
)


async def generate_one(group: str):
    item = await group_domain.get_attributes(group, ['total_treatment'])

    return {
        'fontSizeRatio': 0.5,
        'text': item.get('total_treatment', {}).get('undefined', 0),
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
