# Standard library
import asyncio

# Third party libraries
from backend.domain import (
    project as group_domain,
)

# Local libraries
from analytics import (
    utils,
)
from analytics.colors import (
    RISK,
)


async def generate_one(group: str):
    item = group_domain.get_attributes(group, [
        'open_vulnerabilities',
        'closed_vulnerabilities',
    ])

    return {
        'data': {
            'columns': [
                ['Closed', item.get('closed_vulnerabilities', 0)],
                ['Open', item.get('open_vulnerabilities', 0)],
            ],
            'type': 'pie',
            'colors': {
                'Closed': RISK.more_passive,
                'Open': RISK.more_agressive,
            },
        },
        'legend': {
            'position': 'right',
        },
        'pie': {
            'label': {
                'show': True,
            },
        },
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
