# Standard library
from datetime import datetime
import io
import os

# Third party libraries
from botocore.exceptions import ClientError
import rollbar

# Local libraries
from backend.dal.helpers.s3 import CLIENT as S3_CLIENT  # type: ignore
from __init__ import (
    SERVICES_AWS_S3_DATA_BUCKET as SERVICES_DATA_BUCKET,
)


def get_bill_buffer(*, date: datetime, group: str) -> io.BytesIO:
    year: str = date.strftime('%Y')
    month: str = date.strftime('%m')

    buffer = io.BytesIO()

    key: str = os.path.join('aggregates', 'bills', year, month, f'{group}.csv')

    try:
        S3_CLIENT.download_fileobj(SERVICES_DATA_BUCKET, key, buffer)
    except ClientError:
        rollbar.report_exc_info()
    else:
        buffer.seek(0)

    return buffer
