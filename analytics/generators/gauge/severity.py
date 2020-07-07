# Standard library
import asyncio

# Third party libraries
from backend.api.dataloaders.finding import (
    FindingLoader,
)
from backend.api.dataloaders.project import (
    ProjectLoader as GroupLoader,
)

# Local libraries
from analytics import (
    utils,
)
from analytics.colors import (
    RISK,
)


async def generate_one(group: str):
    group_data = await GroupLoader().load(group)

    findings = await FindingLoader().load_many(
        group_data['findings']
    )

    max_severity_found = 0 if not findings else max(
        finding['severity_score']
        for finding in findings
        if 'current_state' in finding
        and finding['current_state'] != 'DELETED'
    )

    max_open_severity = group_data['attrs'].get('max_open_severity', 0)

    return {
        'color': {
            'pattern': [RISK.more_passive, RISK.more_agressive],
        },
        'data': {
            'columns': [
                ['Max severity found', max_severity_found],
                ['Max open severity', max_open_severity],
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
        'gaugeClearFormat': True,
        'legend': {
            'position': 'right',
        },
    }


async def generate_all():
    for group in utils.iterate_groups():
        data = await generate_one(group)
        utils.json_dump(f'group-{group}.json', data)


if __name__ == '__main__':
    asyncio.run(generate_all())
