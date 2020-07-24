# disable MyPy due to error "boto module has no attribute client"
#  type: ignore

import asyncio
import contextlib
import logging
import os
from tempfile import _TemporaryFileWrapper as TemporaryFileWrapper

import aioboto3
import boto3
from botocore.exceptions import ClientError
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import (
    InMemoryUploadedFile, TemporaryUploadedFile
)

# Local libraries
from backend.utils import apm
from __init__ import (
    FI_AWS_S3_ACCESS_KEY, FI_AWS_S3_SECRET_KEY
)


# Constants
LOGGER = logging.getLogger(__name__)
OPTIONS = dict(
    aws_access_key_id=FI_AWS_S3_ACCESS_KEY,
    aws_secret_access_key=FI_AWS_S3_SECRET_KEY,
    aws_session_token=os.environ.get('AWS_SESSION_TOKEN'),
    region_name='us-east-1',
    service_name='s3',
)
CLIENT = boto3.client(**OPTIONS)


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


async def _send_to_s3(bucket, file_object, file_name):
    success = False
    async with aio_client() as client:
        try:
            repeated_files = await list_files(bucket, file_name)
            await asyncio.gather(*[
                remove_file(bucket, name)
                for name in repeated_files
            ])
            await client.upload_fileobj(file_object, bucket, file_name)
            success = True
        except ClientError as ex:
            LOGGER.exception(ex, extra={'extra': locals()})

    return success


async def upload_memory_file(bucket, file_object, file_name):
    valid_in_memory_files = (
        ContentFile,
        InMemoryUploadedFile,
        TemporaryFileWrapper,
        TemporaryUploadedFile,
    )

    success = False

    if isinstance(file_object, valid_in_memory_files):
        success = await _send_to_s3(bucket, file_object.file, file_name)
    else:
        LOGGER.error(
            'Attempt to upload invalid memory file',
            extra={'extra': locals()})

    return success
