# disable MyPy due to error "boto module has no attribute client"
#  type: ignore

# Standard libraries
import io
import contextlib
import logging
import os

# Third party libraries
from tempfile import _TemporaryFileWrapper as TemporaryFileWrapper

from aioextensions import in_thread

import aioboto3
from botocore.exceptions import ClientError

from starlette.datastructures import UploadFile

# Local libraries
from backend.utils import apm
from back.settings import LOGGING

from __init__ import (
    FI_AWS_S3_ACCESS_KEY, FI_AWS_S3_SECRET_KEY,
    FI_ENVIRONMENT,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
OPTIONS = dict(
    aws_access_key_id=FI_AWS_S3_ACCESS_KEY,
    aws_secret_access_key=FI_AWS_S3_SECRET_KEY,
    aws_session_token=os.environ.get('AWS_SESSION_TOKEN'),
    region_name='us-east-1',
    service_name='s3',
)

if FI_ENVIRONMENT == 'development':
    OPTIONS.pop('aws_session_token', None)
    OPTIONS['endpoint_url'] = 'http://localhost:9000'


@apm.trace()
@contextlib.asynccontextmanager
async def aio_client():
    async with aioboto3.client(**OPTIONS) as client:
        yield client


@apm.trace()
@contextlib.asynccontextmanager
async def aio_resource():
    async with aioboto3.resource(**OPTIONS) as resource:
        yield resource


async def download_file(bucket, file_name, file_path):
    async with aio_client() as client:
        await client.download_file(bucket, file_name, file_path)


async def list_files(bucket, name=None):
    async with aio_client() as client:
        resp = await client.list_objects_v2(Bucket=bucket, Prefix=name)
        key_list = [item['Key'] for item in resp.get('Contents', [])]

    return key_list


async def remove_file(bucket, name):
    success = False
    async with aio_client() as client:
        try:
            response = await client.delete_object(Bucket=bucket, Key=name)
            resp_code = response['ResponseMetadata']['HTTPStatusCode']
            success = resp_code in [200, 204]
        except ClientError as ex:
            LOGGER.exception(ex, extra={'extra': locals()})
    return success


async def _send_to_s3(
    bucket: str,
    file_object: object,
    file_name: str
) -> bool:
    async with aio_client() as client:
        try:
            await client.upload_fileobj(
                file_object,
                bucket,
                file_name
            )

            return True
        except ClientError as ex:
            LOGGER.exception(ex, extra={'extra': locals()})

    return False


async def upload_memory_file(
    bucket: str,
    file_object: object,
    file_name: str
) -> None:
    valid_in_memory_files = (
        TemporaryFileWrapper,
        UploadFile
    )

    success = False

    if isinstance(file_object, valid_in_memory_files):
        bytes_object = io.BytesIO(await in_thread(file_object.file.read))
        success = await _send_to_s3(
            bucket, bytes_object, file_name.lstrip('/')
        )
    else:
        LOGGER.error(
            'Attempt to upload invalid memory file',
            extra={'extra': locals()})

    return success
