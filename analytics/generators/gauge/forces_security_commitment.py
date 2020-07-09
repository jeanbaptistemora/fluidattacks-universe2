# Standard library
import asyncio

# Local libraries
from analytics import (
    utils,
)
from analytics.colors import (
    RISK,
    TREATMENT,
)


async def generate_one(group: str):
    executions = await utils.get_all_time_forces_executions(group)

    executions_in_strict_mode = tuple(
        execution
        for execution in executions
        if execution['strictness'] == 'strict'
    )

    executions_in_any_mode_with_accepted_vulns = tuple(
        execution
        for execution in executions
        for vulns in [execution['vulnerabilities']]
        if vulns['num_of_vulnerabilities_in_accepted_exploits'] > 0
    )

    return {
        'color': {
            'pattern': [RISK.more_passive, TREATMENT.passive],
        },
        'data': {
            'columns': [
                ['Builds in strict mode',
                 len(executions_in_strict_mode)],
                ['Builds with accepted risk',
                 len(executions_in_any_mode_with_accepted_vulns)],
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
        'gaugeClearFormat': True,
        'legend': {
            'position': 'right',
        },
        'paddingRatioTop': 0,
    }


async def generate_all():
    for group in utils.iterate_groups():
        utils.json_dump(
            document=await generate_one(group),
            entity='group',
            subject=group,
        )


if __name__ == '__main__':
    asyncio.run(generate_all())
