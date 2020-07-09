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
        'fontSizeRatio': 0.5,
        'text': non_deleted_findings_count
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
