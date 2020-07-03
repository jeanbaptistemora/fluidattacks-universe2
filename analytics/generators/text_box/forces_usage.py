# Standard library
import asyncio

# Local libraries
from analytics import (
    utils,
)


async def generate_one(group: str):
    executions = await utils.get_all_time_forces_executions(group)

    return {
        'fontSizeRatio': 0.5,
        'text': len(executions),
    }


async def generate_all():
    for group in utils.iterate_groups():
        data = await generate_one(group)
        utils.json_dump(f'group-{group}.json', data)


if __name__ == '__main__':
    asyncio.run(generate_all())
