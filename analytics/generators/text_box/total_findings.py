# Standard library
import asyncio

# Third party libraries
from backend.api.dataloaders.project import (
    ProjectLoader as GroupLoader,
)
from backend.api.dataloaders.finding import (
    FindingLoader,
)

# Local libraries
from analytics import (
    utils,
)


async def generate_one(group: str):
    findings = (await FindingLoader().load_many(
        (await GroupLoader().load(group))['findings']
    ))

    non_deleted_findings_count = sum(
        1
        for finding in findings
        if 'current_state' in finding
        and finding['current_state'] != 'DELETED'
    )

    return {
        'text': non_deleted_findings_count
    }


async def generate_all():
    for group in utils.iterate_groups():
        data = await generate_one(group)
        utils.json_dump(f'group-{group}.json', data)


if __name__ == '__main__':
    asyncio.run(generate_all())
