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

    max_severity_found = 0 if not findings else max(
        finding['severity_score']
        for finding in findings
        if 'current_state' in finding
        and finding['current_state'] != 'DELETED'
    )

    return {
        'color': {
            'pattern': ['#535051'],
        },
        'data': {
            'columns': [
                ['CVSS v3', max_severity_found],
            ],
            'type': 'gauge',
        },
        'gauge': {
            'label': {
                'format': None,
                'show': True,
            },
            'max': 10,
            'min': 0,
        },
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
