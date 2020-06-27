# Third party libraries
from django.core.files.base import ContentFile

# Local libraries
from backend.dal.helpers import (
    cloudfront,
    s3,
)
from backend.exceptions import ErrorUploadingFileS3
from __init__ import (
    FI_CLOUDFRONT_REPORTS_DOMAIN,
    FI_AWS_S3_REPORTS_BUCKET,
)


def sign_url(path: str, minutes: float = 60.0) -> str:
    return cloudfront.sign_url(FI_CLOUDFRONT_REPORTS_DOMAIN, path, minutes)


def upload_report(file_name: str) -> str:
    with open(file_name, 'rb') as file:
        return upload_report_from_file_descriptor(
            ContentFile(file.read(), name=file_name),
        )


def upload_report_from_file_descriptor(report) -> str:
    file_path = report.name
    file_name = file_path.split('_')[-1]

    if not s3.upload_memory_file(  # type: ignore
            FI_AWS_S3_REPORTS_BUCKET, report, file_name):
        raise ErrorUploadingFileS3()

    return file_name
