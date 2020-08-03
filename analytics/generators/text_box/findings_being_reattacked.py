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
    return {
        'fontSizeRatio': 0.5,
        'text': await group_domain.get_pending_closing_check(group),
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
