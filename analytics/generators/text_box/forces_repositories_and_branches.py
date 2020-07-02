# Standard library
import asyncio

# Local libraries
from analytics import (
    utils,
)


async def generate_one(group: str):
    executions = await utils.get_last_week_forces_executions(group)

    return {
        'text': len(set(
            execution['git_repo'] + execution['git_branch']
            for execution in executions
        ))
    }


async def generate_all():
    for group in utils.iterate_groups():
        data = await generate_one(group)
        utils.json_dump(f'group-{group}.json', data)


if __name__ == '__main__':
    asyncio.run(generate_all())
