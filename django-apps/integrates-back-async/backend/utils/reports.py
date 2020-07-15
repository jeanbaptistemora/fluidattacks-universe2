# Standard library
from uuid import uuid4 as uuid

# Third party libraries
from asgiref.sync import async_to_sync
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


def sign_url(path: str, minutes: float = 60.0) -> str:
    return cloudfront.sign_url(FI_CLOUDFRONT_REPORTS_DOMAIN, path, minutes)


async def sign(path: str, ttl: float) -> str:
    return await aio.ensure_io_bound(
        cloudfront.sign_url,
        FI_CLOUDFRONT_REPORTS_DOMAIN,
        path,
        ttl / 60,
    )


def upload_report(file_name: str) -> str:
    with open(file_name, 'rb') as file:
        return upload_report_from_file_descriptor(
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


@async_to_sync
async def upload_report_from_file_descriptor(report) -> str:
    file_path = report.name
    file_name = file_path.split('_')[-1]

    if not await s3.upload_memory_file(  # type: ignore
            FI_AWS_S3_REPORTS_BUCKET, report, file_name):
        raise ErrorUploadingFileS3()

    return file_name
