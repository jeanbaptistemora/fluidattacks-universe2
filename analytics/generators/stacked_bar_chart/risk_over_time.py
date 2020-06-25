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

        for accepted, closed, found in zip(
            group_accepted_over_time,
            group_closed_over_time,
            group_found_over_time,
        ):
            data.append(dict(
                accepted=accepted['y'],
                closed=closed['y'],
                opened=found['y'] - closed['y'] - accepted['y'],
                name=found['x'],
                total=found['y'],
            ))
    else:
        print(f'[WARNING] {group} has no remediated_over_time attribute')

    return dict(
        data=dict(
            x='date',
            columns=[
                ['date'] + [datum['name'] for datum in data],
                ['Accepted'] + [datum['accepted'] for datum in data],
                ['Closed'] + [datum['closed'] for datum in data],
                ['Opened'] + [datum['opened'] for datum in data],
            ],
            groups=[
                ['Accepted', 'Closed', 'Opened'],
            ],
            colors={
                'Closed': '#eae2b7',
                'Accepted': '#fcbf49',
                'Opened': '#d62828',
            },
            type='bar',
        ),
        axis=dict(
            x=dict(
                tick=dict(
                    centered=True,
                    multiline=False,
                    rotate=8,
                ),
                type='category',
            ),
        ),
        grid=dict(
            y=dict(
                show=True,
            ),
        ),
    )


async def generate_all():
    for group in utils.iterate_groups():
        data = await generate_one(group)
        utils.json_dump(f'group-{group}.json', data)


if __name__ == '__main__':
    asyncio.run(generate_all())
