# Standard library
import io
import logging
import os
from datetime import datetime

# Third party libraries
from botocore.exceptions import ClientError

# Local libraries
from backend.dal.helpers.s3 import aio_client  # type: ignore
from backend.utils import (
    apm,
)
from __init__ import (
    SERVICES_AWS_S3_DATA_BUCKET as SERVICES_DATA_BUCKET,
)


# Constants
LOGGER = logging.getLogger(__name__)


@apm.trace()
async def get_bill_buffer(*, date: datetime, group: str) -> io.BytesIO:
    year: str = date.strftime('%Y')
    month: str = date.strftime('%m')

    buffer = io.BytesIO()

    key: str = os.path.join('aggregates', 'bills', year, month, f'{group}.csv')

    try:
        async with aio_client() as client:
            await client.download_fileobj(SERVICES_DATA_BUCKET, key, buffer)
    except ClientError as ex:
        LOGGER.exception(ex)
    else:
        buffer.seek(0)

    return buffer
