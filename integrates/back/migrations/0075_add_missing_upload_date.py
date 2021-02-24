"""
This migration aims to add upload_date to evidence files when missing,
taking it from LastModified

Execution Time:    2021-02-24 at 08:24:07 UTC-05
Finalization Time: 2021-02-24 at 08:25:51 UTC-05
"""
# Standard library
from typing import (
    Dict,
    List,
)

# Third party libraries
from aioextensions import (
    collect,
    run,
)

# Local libraries
from backend.api.dataloaders.event import EventLoader
from backend.dal import event as event_dal
from backend.dal.helpers.s3 import aio_client
from backend.domain.project import (
    get_alive_projects,
    list_events,
)
from backend.typing import Event
from backend.utils import datetime as datetime_utils
from __init__ import FI_AWS_S3_BUCKET


async def add_missing_upload_date(event: Event) -> None:
    event_id = str(event['id'])
    group_name = str(event['project_name'])
    event_evidences = ['evidence', 'evidence_file']
    key_list = []
    date_list = []
    coroutines = []
    event_prefix = f'{group_name}/{event_id}/'
    async with aio_client() as client:
        resp = await client.list_objects_v2(
            Bucket=FI_AWS_S3_BUCKET, Prefix=event_prefix
        )
        key_list = [item['Key'] for item in resp.get('Contents', [])]
        date_list = [item['LastModified'] for item in resp.get('Contents', [])]

    for evidence in event_evidences:
        if evidence in event and f'{evidence}_date' not in event:
            file_url = event_prefix + event[evidence]
            if file_url in key_list:
                file_index = key_list.index(file_url)
                unaware_datetime = date_list[file_index]
                upload_date = datetime_utils.get_as_str(unaware_datetime)
                coroutines.append(
                    event_dal.update(
                        event_id, {f'{evidence}_date': upload_date}
                    )
                )

    if len(coroutines) > 0:
        print(f'should update event {event_id}')
        await collect(coroutines)


async def get_groups_events(group_name: str) -> None:
    event_ids = await list_events(group_name)
    events = await EventLoader().load_many(event_ids)

    await collect(map(add_missing_upload_date, events), workers=10)


async def main() -> None:
    groups = await get_alive_projects()
    await collect(map(get_groups_events, groups), workers=10)


if __name__ == '__main__':
    run(main())
