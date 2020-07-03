# Standard library
import asyncio

# Third party libraries
from backend.domain import (
    project as group_domain,
)
from backend.utils import (
    aio,
)

# Local libraries
from analytics import (
    utils,
)


async def generate_one(group: str):
    return {
        'fontSizeRatio': 0.5,
        'text': await aio.ensure_io_bound(
            group_domain.get_pending_closing_check, group,
        ),
    }


async def generate_all():
    for group in utils.iterate_groups():
        data = await generate_one(group)
        utils.json_dump(f'group-{group}.json', data)


if __name__ == '__main__':
    asyncio.run(generate_all())
