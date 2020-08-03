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
    item = await group_domain.get_attributes(group, ['total_treatment'])

    treatment = item.get('total_treatment', {})

    translations = {
        'acceptedUndefined': 'Eternally accepted',
        'accepted': 'Temporarily Accepted',
        'inProgress': 'In Progress',
        'undefined': 'Not defined',
    }

    return {
        'data': {
            'columns': [
                [translations[column], treatment.get(column, 0)]
                for column in translations
            ],
            'type': 'pie',
            'colors': {
                'Eternally accepted': TREATMENT.more_passive,
                'Temporarily Accepted': TREATMENT.passive,
                'In Progress': TREATMENT.neutral,
                'Not defined': TREATMENT.more_agressive,
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
    async for group in utils.iterate_groups():
        utils.json_dump(
            document=await generate_one(group),
            entity='group',
            subject=group,
        )


if __name__ == '__main__':
    asyncio.run(generate_all())
