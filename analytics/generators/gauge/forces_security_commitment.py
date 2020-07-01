# Standard library
import asyncio

# Local libraries
from analytics import (
    utils,
)


async def generate_one(group: str):
    executions = await utils.get_last_week_forces_executions(group)

    executions_in_strict_mode = tuple(
        execution
        for execution in executions
        if execution['strictness'] == 'strict'
    )

    return {
        'color': {
            'pattern': ['#535051'],
        },
        'data': {
            'columns': [
                ['Builds in strict mode', len(executions_in_strict_mode)],
            ],
            'type': 'gauge',
        },
        'gauge': {
            'label': {
                'format': None,
                'show': True,
            },
            'max': len(executions),
            'min': 0,
        },
        'gaugeClearFormat': False,
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
