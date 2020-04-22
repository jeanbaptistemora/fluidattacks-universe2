from backend.dal.helpers import cloudfront
from backend.exceptions import ErrorUploadingFileS3
from backend.utils import reports
from __init__ import FI_CLOUDFRONT_REPORTS_DOMAIN


def sign_url(file_name: str) -> str:
    return cloudfront.sign_url(
        FI_CLOUDFRONT_REPORTS_DOMAIN, file_name, 60.0)


def upload_report(file_name: str) -> str:
    success, uploaded_file_name = reports.upload_report(file_name)
    if not success:
        raise ErrorUploadingFileS3()
    return uploaded_file_name
