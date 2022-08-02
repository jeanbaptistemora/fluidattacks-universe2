from aiohttp.client_exceptions import (
    ClientPayloadError,
)
from botocore.exceptions import (
    ClientError,
)
from context import (
    CI_COMMIT_REF_NAME,
    FI_AWS_S3_ANALYTICS_BUCKET as BUCKET_ANALYTICS,
)
from custom_exceptions import (
    DocumentNotFound,
    SnapshotNotFound,
)
import io
import logging
import logging.config
from s3.resource import (
    get_s3_resource,
)
from settings import (
    LOGGING,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def get_document(key: str) -> str:
    key = f"{CI_COMMIT_REF_NAME}/documents/{key}"
    client = await get_s3_resource()

    with io.BytesIO() as stream:

        # Stream the download to an in-memory buffer
        try:
            await client.download_fileobj(BUCKET_ANALYTICS, key, stream)
        except ClientError as ex:
            raise DocumentNotFound() from ex

        # Return pointer to begin-of-file
        stream.seek(0)

        # Documents are guaranteed to be UTF-8 encoded
        return stream.read().decode()


async def get_snapshot(key: str) -> bytes:
    key = f"{CI_COMMIT_REF_NAME}/snapshots/{key}"
    client = await get_s3_resource()

    with io.BytesIO() as stream:

        # Stream the download to an in-memory buffer
        try:
            await client.download_fileobj(BUCKET_ANALYTICS, key, stream)
        except (ClientError, ClientPayloadError) as ex:
            LOGGER.exception(ex, extra=dict(extra=locals()))
            raise SnapshotNotFound() from ex

        # Return pointer to begin-of-file
        stream.seek(0)

        return stream.read()
