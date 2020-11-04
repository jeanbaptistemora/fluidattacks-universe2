# disable MyPy due to error "boto module has no attribute client"
#  type: ignore

import contextlib
import logging
import os
from tempfile import _TemporaryFileWrapper as TemporaryFileWrapper

import aioboto3
from botocore.exceptions import ClientError
from django.core.files.base import ContentFile
from starlette.datastructures import UploadFile

# Local libraries
from backend.utils import apm
from fluidintegrates.settings import LOGGING
from __init__ import (
    FI_AWS_S3_ACCESS_KEY, FI_AWS_S3_SECRET_KEY,
    FI_ENVIRONMENT, FI_MINIO_LOCAL_ENABLED
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

MINIO_OFF = False  # turn off MinIO until S3 is cleaned

if FI_ENVIRONMENT == 'development' and FI_MINIO_LOCAL_ENABLED == 'true' \
        and MINIO_OFF:
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
        ContentFile,
        TemporaryFileWrapper,
        UploadFile
    )

    success = False

    if isinstance(file_object, valid_in_memory_files):
        success = await _send_to_s3(bucket, file_object.file, file_name)
    else:
        LOGGER.error(
            'Attempt to upload invalid memory file',
            extra={'extra': locals()})

    return success
