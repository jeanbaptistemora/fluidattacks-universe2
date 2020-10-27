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
            vulns.get('num_of_vulnerabilities_in_exploits', 0) +
            vulns.get('num_of_vulnerabilities_in_integrates_exploits', 0) +
            vulns.get('num_of_vulnerabilities_in_accepted_exploits', 0) +
            vulns.get('num_of_accepted_vulnerabilities', 0) +
            vulns.get('num_of_open_vulnerabilities', 0) +
            vulns.get('num_of_closed_vulnerabilities', 0)
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
