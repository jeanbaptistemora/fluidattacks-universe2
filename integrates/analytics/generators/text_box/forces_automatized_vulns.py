# Standard library

# Third party libraries
from aioextensions import run

# Local libraries
from analytics import (
    utils,
)


async def generate_one(group: str):
    executions = await utils.get_all_time_forces_executions(group)

    return {
        'fontSizeRatio': 0.5,
        'text': sum(
            vulns['num_of_vulnerabilities_in_exploits'] +
            vulns['num_of_vulnerabilities_in_integrates_exploits'] +
            vulns['num_of_vulnerabilities_in_accepted_exploits']
            for execution in executions
            for vulns in [execution['vulnerabilities']]
        )
    }


async def generate_all():
    async for group in utils.iterate_groups():
        utils.json_dump(
            document=await generate_one(group),
            entity='group',
            subject=group,
        )


if __name__ == '__main__':
    run(generate_all())
