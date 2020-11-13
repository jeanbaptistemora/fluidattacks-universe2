"""
This migration delete the duplicated evidences on S3
for unittesting
Execution Time:    2020-10-19 13:20:56 UTC-5
Finalization Time: 2020-10-19 13:21:24 UTC-5
"""
# disable MyPy due to error "boto module has no attribute client"
import aioboto3
import contextlib
import logging
import os
import time

from backend.dal.helpers import s3
from backend.utils import apm
from botocore.exceptions import ClientError
from fluidintegrates.settings import LOGGING
from __init__ import (
    FI_AWS_S3_ACCESS_KEY, FI_AWS_S3_SECRET_KEY
)
from aioextensions import (
    collect,
    in_thread,
    run,
)
from typing import (
    List,
    cast,
)
from collections.abc import AsyncGenerator

# Constants
logging.config.dictConfig(LOGGING)
STAGE = os.environ['STAGE']
BUCKET = 'fluidintegrates.evidences'
LOGGER = logging.getLogger(__name__)
OPTIONS = dict(
    aws_access_key_id=FI_AWS_S3_ACCESS_KEY,
    aws_secret_access_key=FI_AWS_S3_SECRET_KEY,
    aws_session_token=os.environ.get('AWS_SESSION_TOKEN'),
    region_name='us-east-1',
    service_name='s3',
)


@apm.trace()
@contextlib.asynccontextmanager
async def aio_client():  # type: ignore
    async with aioboto3.client(**OPTIONS) as client:
        yield client


async def get_all_project_evidences(name: str) -> List[str]:
    async with aio_client() as client:
        continuation_token = None
        key_list: List[str] = []
        while True:
            if continuation_token:
                resp = await client.list_objects_v2(
                    Bucket=BUCKET,
                    Prefix=name,
                    ContinuationToken=continuation_token
                )
            else:
                resp = await client.list_objects_v2(
                    Bucket=BUCKET,
                    Prefix=name
                )
            key_list += [item['Key'] for item in resp.get('Contents', [])]
            if not resp.get('IsTruncated'):
                break
            continuation_token = resp.get('NextContinuationToken')
    return key_list


async def remove_file(name: str) -> int:
    print(f'[INFO] Deleting evidence {name}')
    success = False
    async with aio_client() as client:
        try:
            response = await client.delete_object(Bucket=BUCKET, Key=name)
            resp_code = response['ResponseMetadata']['HTTPStatusCode']
            success = resp_code in [200, 204]
        except ClientError as ex:
            LOGGER.exception(ex, extra={'extra': locals()})
    return success


async def main() -> None:
    print('[INFO] starting migration 0031')
    all_evidences = await get_all_project_evidences('unittesting')
    mock_findings = [
        '988493279',  # findings on dev
        '422286126',  # findings on dev
        '436992569',  # findings on dev
        '463461507',  # findings on dev
        '463558592',  # findings on dev
        '457497316',  # findings on dev
        '695730302',  # findings on prod
        '626277119',  # findings on prod
        '763866292',  # findings on prod
        '724980983',  # findings on prod
        '602606668',  # findings on prod
        '830307016',  # findings on prod
        '679777842',  # findings on prod
        '563324181',  # findings on prod
        '835563730',  # findings on prod
        '772927078',  # findings on prod
        '719218120',  # findings on prod
    ]
    evidences: List[str] = []
    for evidence in all_evidences:
        if evidence.split("/")[1] not in mock_findings:
            evidences.append(evidence)
    evidences.sort()

    if STAGE == 'test':
        results = await collect([
            in_thread(
                print,
                f'[INFO] Evidence {evidence} will be deleted'
            )
            for evidence in evidences
        ])
        print(
            '[INFO] Total evidences to delete: '
            f'{len(evidences)}'
        )
        print('[INFO] migration 0031 test finished')

    else:
        results = await collect([
            await in_thread(remove_file, evidence)
            for evidence in evidences
        ])
        print(
            '[INFO] Total evidences deleted: '
            f'{sum(results)} of {len(evidences)}'
        )
        print('[INFO] migration 0031 apply finished')
        pass

if __name__ == '__main__':
    execution_time = time.strftime(
        'Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z'
    )
    run(main())
    finalization_time = time.strftime(
        'Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z'
    )
    print(f'{execution_time}\n{finalization_time}')
