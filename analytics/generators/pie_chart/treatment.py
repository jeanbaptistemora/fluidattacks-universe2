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


async def generate_one(group: str):
    item = group_domain.get_attributes(group, ['total_treatment'])

    treatment = item.get('total_treatment', {
        'accepted': 0,
        'inProgress': 0,
        'acceptedUndefined': 0,
        'undefined': 0,
    })

    translations = {
        'accepted': 'Accepted',
        'inProgress': 'In Progress',
        'acceptedUndefined': 'Eternally accepted',
        'undefined': 'Not defined',
    }

    return {
        'data': {
            'columns': [
                [translations[name], value]
                for name, value in treatment.items()
            ],
            'type': 'pie',
            'colors': {
                'Accepted': '#999797',
                'Eternally accepted': '#000000',
                'In Progress': '#FF9034',
                'Not defined': '#A70762',
            },
        },
        'pie': {
            'label': {
                'show': False,
            },
        },
    }


async def generate_all():
    for group in utils.iterate_groups():
        data = await generate_one(group)
        utils.json_dump(f'group-{group}.json', data)


if __name__ == '__main__':
    asyncio.run(generate_all())
