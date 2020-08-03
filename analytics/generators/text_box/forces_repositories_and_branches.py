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
        'text': len(set(
            execution['git_repo'] + execution['git_branch']
            for execution in executions
        ))
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
