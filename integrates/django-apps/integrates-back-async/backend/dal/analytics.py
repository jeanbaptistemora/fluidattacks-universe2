# Standard library
import io

# Local libraries
from backend.dal.helpers.s3 import (  # type: ignore
    aio_client,
)
from backend.utils import (
    apm,
)
from __init__ import (
    CI_COMMIT_REF_NAME,
    FI_AWS_S3_ANALYTICS_BUCKET as BUCKET_ANALYTICS,
)


@apm.trace()
async def get_document(key: str) -> str:
    key = f'{CI_COMMIT_REF_NAME}/documents/{key}'

    with io.BytesIO() as stream:

        # Stream the download to an in-memory buffer
        async with aio_client() as client:
            await client.download_fileobj(BUCKET_ANALYTICS, key, stream)

        # Return pointer to begin-of-file
        stream.seek(0)

        # Documents are guaranteed to be UTF-8 encoded
        return stream.read().decode()


@apm.trace()
async def get_snapshot(key: str) -> bytes:
    key = f'{CI_COMMIT_REF_NAME}/snapshots/{key}'

    with io.BytesIO() as stream:

        # Stream the download to an in-memory buffer
        async with aio_client() as client:
            await client.download_fileobj(BUCKET_ANALYTICS, key, stream)

        # Return pointer to begin-of-file
        stream.seek(0)

        return stream.read()
