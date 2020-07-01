# Standard library
import asyncio

# Local libraries
from analytics import (
    utils,
)
from analytics.colors import (
    RISK,
)


async def generate_one(group: str):
    executions = await utils.get_last_week_forces_executions(group)

    executions_in_any_mode_with_vulns = tuple(
        execution
        for execution in executions
        for vulns in [execution['vulnerabilities']]
        if vulns['num_of_vulnerabilities_in_exploits'] > 0
        or vulns['num_of_vulnerabilities_in_integrates_exploits'] > 0
    )

    return {
        'color': {
            'pattern': [RISK.more_agressive],
        },
        'data': {
            'columns': [
                ['Builds with security issues',
                 len(executions_in_any_mode_with_vulns)],
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
