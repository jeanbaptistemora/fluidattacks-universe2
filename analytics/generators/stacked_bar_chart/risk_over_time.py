# Standard library
import asyncio
from datetime import datetime
from typing import (
    Dict,
    List,
)

# Third party libraries
from async_lru import alru_cache
from backend.api.dataloaders.project import ProjectLoader
from backend.utils import (
    aio,
)

# Local libraries
from analytics import (
    utils,
)
from analytics.colors import (
    RISK,
)

# Constants
DATE_FMT: str = '%Y - %m - %d'

# Let's no over think it
MONTH_TO_NUMBER = {
    'Jan': 1,
    'Feb': 2,
    'Mar': 3,
    'Apr': 4,
    'May': 5,
    'Jun': 6,
    'Jul': 7,
    'Aug': 8,
    'Sep': 9,
    'Oct': 10,
    'Nov': 11,
    'Dec': 12,
}


def translate_date(date_str: str) -> datetime:
    # No, there is no smarter way because of locales and that weird format

    parts = date_str.replace(',', '').replace('- ', '').split(' ')

    if len(parts) == 6:
        date_year, date_month, date_day = parts[2], parts[0], parts[1]
    elif len(parts) == 5:
        date_year, date_month, date_day = parts[4], parts[0], parts[1]
    elif len(parts) == 4:
        date_year, date_month, date_day = parts[3], parts[0], parts[1]
    else:
        raise ValueError(f'Unexpected number of parts: {parts}')

    return datetime(int(date_year), MONTH_TO_NUMBER[date_month], int(date_day))


@alru_cache(maxsize=None, typed=True)
async def get_group_document(group: str) -> Dict[str, Dict[str, float]]:
    data: List[list] = []

    group_loader = ProjectLoader()
    group_data = await group_loader.load(group)
    group_over_time = [
        # Last 12 weeks
        elements[-12:]
        for elements in group_data['attrs'].get('remediated_over_time', [])
    ]

    if group_over_time:
        group_found_over_time = group_over_time[0]
        group_closed_over_time = group_over_time[1]
        group_accepted_over_time = group_over_time[2]

        for accepted, closed, found in zip(
            group_accepted_over_time,
            group_closed_over_time,
            group_found_over_time,
        ):
            data.append(dict(
                accepted=accepted['y'],
                closed=closed['y'],
                opened=found['y'] - closed['y'] - accepted['y'],
                date=translate_date(found['x']),
                total=found['y'],
            ))
    else:
        print(f'[WARNING] {group} has no remediated_over_time attribute')

    return {
        'date': {
            datum['date']: 0
            for datum in data
        },
        'Closed': {
            datum['date']: datum['closed']
            for datum in data
        },
        'Closed + Open with accepted treatment': {
            datum['date']: datum['closed'] + datum['accepted']
            for datum in data
        },
        'Closed + Open': {
            datum['date']: (
                datum['closed'] + datum['accepted'] + datum['opened']
            )
            for datum in data
        },
    }


async def get_many_groups_document(
    groups: str,
) -> Dict[str, Dict[str, float]]:
    group_documents = await aio.materialize(map(get_group_document, groups))

    all_dates: List[datetime] = sorted(set(
        date
        for group_document in group_documents
        for date in group_document['date']
    ))

    # fill missing dates with it's more near value to the left
    for group_document in group_documents:
        for name in group_document:
            last_date = None
            for date in all_dates:
                if date in group_document[name]:
                    last_date = date
                elif last_date:
                    group_document[name][date] = \
                        group_document[name][last_date]
                else:
                    group_document[name][date] = 0

    return {
        name: {
            date: sum(
                group_document[name].get(date, 0)
                for group_document in group_documents
            )
            for date in all_dates
        }
        for name in [
            'date',
            'Closed',
            'Closed + Open with accepted treatment',
            'Closed + Open',
        ]
    }


def format_document(document: object) -> dict:
    return dict(
        data=dict(
            x='date',
            columns=[
                [name] + [
                    date.strftime(DATE_FMT)
                    if name == 'date'
                    else document[name][date]
                    for date in document['date']
                ]
                for name in document
            ],
            colors={
                'Closed': RISK.more_passive,
                'Closed + Open with accepted treatment': RISK.agressive,
                'Closed + Open': RISK.more_agressive,
            },
            types={
                'Closed': 'line',
                'Closed + Open with accepted treatment': 'line',
                'Closed + Open': 'line',
            },
        ),
        axis=dict(
            x=dict(
                tick=dict(
                    centered=True,
                    multiline=False,
                    rotate=12,
                ),
                type='category',
            ),
        ),
        grid=dict(
            x=dict(
                show=True,
            ),
            y=dict(
                show=True,
            ),
        ),
        legend=dict(
            position='bottom',
        ),
        point=dict(
            focus=dict(
                expand=dict(
                    enabled=True,
                ),
            ),
            r=5,
        ),
    )


async def generate_all():
    for group in utils.iterate_groups():
        utils.json_dump(
            document=format_document(
                document=await get_group_document(group),
            ),
            entity='group',
            subject=group,
        )

    async for org_id, _, org_groups in (
        utils.iterate_organizations_and_groups()
    ):
        utils.json_dump(
            document=format_document(
                document=await get_many_groups_document(org_groups),
            ),
            entity='organization',
            subject=org_id,
        )


if __name__ == '__main__':
    asyncio.run(generate_all())
