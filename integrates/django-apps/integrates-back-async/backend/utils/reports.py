# Standard library
import asyncio
import logging
from typing import Dict
from uuid import uuid4 as uuid

# Third party libraries
from django.core.files.base import ContentFile

# Local libraries
from backend.dal.helpers import (
    cloudfront,
    s3,
)
from backend.utils import (
    aio,
)
from backend.exceptions import ErrorUploadingFileS3
from __init__ import (
    FI_CLOUDFRONT_REPORTS_DOMAIN,
    FI_AWS_S3_REPORTS_BUCKET,
)

# Constants
LOGGER = logging.getLogger(__name__)


async def sign_url(path: str, minutes: float = 60.0) -> str:
    return await aio.ensure_io_bound(
        cloudfront.sign_url, FI_CLOUDFRONT_REPORTS_DOMAIN, path, minutes
    )


async def sign(path: str, ttl: float) -> str:
    return await aio.ensure_io_bound(
        cloudfront.sign_url,
        FI_CLOUDFRONT_REPORTS_DOMAIN,
        path,
        ttl / 60,
    )


async def upload_report(file_name: str) -> str:
    with open(file_name, 'rb') as file:
        return await upload_report_from_file_descriptor(
            ContentFile(file.read(), name=file_name),
        )


async def expose_bytes_as_url(
    *,
    content: bytes,
    ext: str = '',
    ttl: float,
) -> str:
    file_name: str = uuid().hex

    if ext:
        file_name += '.' + ext

    if not await s3.upload_memory_file(  # type: ignore
        FI_AWS_S3_REPORTS_BUCKET,
        ContentFile(content, name=file_name),
        file_name,
    ):
        raise ErrorUploadingFileS3()

    return await sign(path=file_name, ttl=ttl)


async def upload_report_from_file_descriptor(report) -> str:
    file_path = report.name
    file_name = file_path.split('_')[-1]

    if not await s3.upload_memory_file(  # type: ignore
            FI_AWS_S3_REPORTS_BUCKET, report, file_name):
        raise ErrorUploadingFileS3()

    return file_name


def reports_exception_handler(
    _: asyncio.AbstractEventLoop,
    context: Dict[str, str]
) -> None:
    """
    Catches any exception raised in report generation
    process and reports information to bugsnag
    """

    exception = context.get('exception', 'not provided')
    error_msg = (
        f'Message: {context.get("message", "")} '
        f'Exception: \'{exception}\''
    )
    LOGGER.error(
        error_msg,
        extra={
            'extra': {
                'exception': exception
            }
        }
    )


def patch_loop_exception_handler() -> None:
    asyncio.get_event_loop().set_exception_handler(reports_exception_handler)
