import io
import logging
import logging.config
import os
from datetime import datetime

from botocore.exceptions import ClientError

from __init__ import SERVICES_AWS_S3_DATA_BUCKET as SERVICES_DATA_BUCKET
from s3.operations import aio_client
from settings import LOGGING


logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def get_bill_buffer(*, date: datetime, group: str) -> io.BytesIO:
    year: str = date.strftime("%Y")
    month: str = date.strftime("%m")
    # The day is also available after 2019-09 in case it's needed

    buffer = io.BytesIO()

    key: str = os.path.join("bills", year, month, f"{group}.csv")

    try:
        async with aio_client() as client:
            await client.download_fileobj(SERVICES_DATA_BUCKET, key, buffer)
    except ClientError as ex:
        LOGGER.exception(ex, extra=dict(extra=locals()))
    else:
        buffer.seek(0)

    return buffer
