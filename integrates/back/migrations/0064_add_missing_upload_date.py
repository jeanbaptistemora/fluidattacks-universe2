"""
This migration aims to add upload_date when missing,
taking it from LastModified

Execution Time: 
Finalization Time: 
"""
# Standard library
from itertools import chain
import os
from typing import (
    Dict,
    List,
)

# Third party libraries
from aioextensions import (
    collect,
    run,
)
from more_itertools import chunked

# Local libraries
from backend.api.dataloaders.project import ProjectLoader as GroupLoader
from backend.dal import finding as finding_dal
from backend.dal.helpers.s3 import (
    aio_client,
)
from backend.domain.project import get_active_projects
from backend.typing import Finding
from backend.utils import datetime as datetime_utils
from __init__ import FI_AWS_S3_BUCKET
STAGE: str = os.environ['STAGE']


async def _remove_treatment_manager(finding: Dict[str, Finding]) -> None:
    finding_id = str(finding['finding_id'])
    group_name = str(finding['project_name'])
    key_list = []
    date_list = []
    coroutines = []
    finding_prefix = f'{group_name}/{finding_id}/'
    async with aio_client() as client:
        resp = await client.list_objects_v2(
            Bucket=FI_AWS_S3_BUCKET, Prefix=finding_prefix
        )
        key_list = [item['Key'] for item in resp.get('Contents', [])]
        date_list = [item['LastModified'] for item in resp.get('Contents', [])]

    for index, evidence in enumerate(finding.get('files', [])):
        if 'upload_date' not in evidence and evidence.get('file_url'):
            file_url = finding_prefix + evidence['file_url']
            if file_url in key_list:
                file_index = key_list.index(file_url)
                unaware_datetime = date_list[file_index]
                upload_date = datetime_utils.get_as_str(unaware_datetime)
                coroutines.append(
                    finding_dal.update(
                        finding_id,
                        {f'files[{index}].upload_date': upload_date}
                    )
                )

    if len(coroutines) > 1:
        if STAGE == 'apply':
            await collect(coroutines)
        else:
            print(f'should update finding {finding_id}')


async def remove_treatment_manager(groups: List[str]) -> None:
    groups_data = await GroupLoader().load_many(groups)
    findings_ids = list(
        chain.from_iterable(
            group_data['findings'] + group_data['drafts']
            for group_data in groups_data
        )
    )
    findings = await collect(map(finding_dal.get_finding, findings_ids))

    await collect(
        map(_remove_treatment_manager, findings),
        workers=10
    )


async def main() -> None:
    groups = await get_active_projects()
    await collect(
        [remove_treatment_manager(list_group)
         for list_group in chunked(groups, 5)],
        workers=10
    )


if __name__ == '__main__':
    run(main())
