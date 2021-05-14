# Standard library

# Third party libraries
from aioextensions import run

# Local libraries
from charts import utils
from charts.colors import RISK


async def generate_one(group: str) -> dict:
    executions = await utils.get_all_time_forces_executions(group)

    executions_in_strict_mode = tuple(
        execution
        for execution in executions
        if execution['strictness'] == 'strict'
    )

    executions_in_any_mode_with_vulns = tuple(
        execution
        for execution in executions
        for vulns in [execution['vulnerabilities']]
        if vulns.get('num_of_vulnerabilities_in_exploits', 0) > 0
        or vulns.get('num_of_vulnerabilities_in_integrates_exploits', 0) > 0
        or vulns.get('num_of_vulnerabilities_in_accepted_exploits', 0) > 0
        or vulns.get('num_of_open_vulnerabilities', 0) > 0
        or vulns.get('num_of_accepted_vulnerabilities', 0) > 0
    )

    executions_in_strict_mode_with_vulns = tuple(
        execution
        for execution in executions_in_strict_mode
        for vulns in [execution['vulnerabilities']]
        if vulns.get('num_of_vulnerabilities_in_exploits', 0) > 0
        or vulns.get('num_of_vulnerabilities_in_integrates_exploits', 0) > 0
        or vulns.get('num_of_open_vulnerabilities', 0) > 0
    )

    return {
        'color': {
            'pattern': [RISK.more_passive, RISK.more_agressive],
        },
        'data': {
            'columns': [
                ['Vulnerable builds prevented',
                 len(executions_in_strict_mode_with_vulns)],
                ['Vulnerable builds',
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
        'gaugeClearFormat': True,
        'legend': {
            'position': 'right',
        },
        'paddingRatioTop': 0,
    }


async def generate_all() -> None:
    async for group in utils.iterate_groups():
        utils.json_dump(
            document=await generate_one(group),
            entity='group',
            subject=group,
        )


if __name__ == '__main__':
    run(generate_all())
