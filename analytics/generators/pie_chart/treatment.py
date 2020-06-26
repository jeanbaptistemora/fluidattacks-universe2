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
    TREATMENT,
)


async def generate_one(group: str):
    item = group_domain.get_attributes(group, ['total_treatment'])

    treatment = item.get('total_treatment', {})

    translations = {
        'undefined': 'Not defined',
        'inProgress': 'In Progress',
        'accepted': 'Accepted',
        'acceptedUndefined': 'Eternally accepted',
    }

    return {
        'data': {
            'columns': [
                [translations[column], treatment.get(column, 0)]
                for column in translations
            ],
            'type': 'pie',
            'colors': {
                'Accepted': TREATMENT.passive,
                'Eternally accepted': TREATMENT.more_passive,
                'In Progress': TREATMENT.neutral,
                'Not defined': TREATMENT.more_agressive,
            },
        },
        'pie': {
            'label': {
                'show': True,
            },
        },
    }


async def generate_all():
    for group in utils.iterate_groups():
        data = await generate_one(group)
        utils.json_dump(f'group-{group}.json', data)


if __name__ == '__main__':
    asyncio.run(generate_all())
