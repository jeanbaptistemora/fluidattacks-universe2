# Standard library
import asyncio

# Local libraries
from analytics import (
    utils,
)


async def generate_one(group: str):
    executions = await utils.get_last_week_forces_executions(group)

    return {
        'text': sum(
            vulns['num_of_vulnerabilities_in_exploits'] +
            vulns['num_of_vulnerabilities_in_integrates_exploits'] +
            vulns['num_of_vulnerabilities_in_accepted_exploits']
            for execution in executions
            for vulns in [execution['vulnerabilities']]
        )
    }


async def generate_all():
    for group in utils.iterate_groups():
        data = await generate_one(group)
        utils.json_dump(f'group-{group}.json', data)


if __name__ == '__main__':
    asyncio.run(generate_all())
