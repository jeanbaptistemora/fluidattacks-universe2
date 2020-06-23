# Standard library
import asyncio

# Third party libraries
from backend.api.dataloaders.project import ProjectLoader

# Local libraries
from analytics import (
    utils,
)


async def generate_one(group: str):
    data: list = []

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
        group_opened_over_time = [
            dict(x=found['x'], y=found['y'] - closed['y'] - accepted['y'])
            for found, closed, accepted in zip(
                group_found_over_time,
                group_closed_over_time,
                group_accepted_over_time
            )
        ]
        min_iterable_len = len(group_opened_over_time)

        for category, iterable in [
            ('opened', group_opened_over_time[0:min_iterable_len]),
            ('accepted', group_accepted_over_time[0:min_iterable_len]),
            ('closed', group_closed_over_time[0:min_iterable_len]),
        ]:
            data.extend(
                dict(
                    category=category,
                    count=element['y'],
                    date=element['x'],
                )
                for element in iterable
            )
    else:
        print(f'[WARNING] {group} has no remediated_over_time attribute')

    return data


async def generate_all():
    for group in utils.iterate_groups():
        data = await generate_one(group)
        utils.json_dump(f'group-{group}.json', data)


if __name__ == '__main__':
    asyncio.run(generate_all())
