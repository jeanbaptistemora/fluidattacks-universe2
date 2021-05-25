import io

from botocore.exceptions import ClientError

from context import (
    CI_COMMIT_REF_NAME,
    FI_AWS_S3_ANALYTICS_BUCKET as BUCKET_ANALYTICS,
)
from custom_exceptions import DocumentNotFound
from newutils import apm
from s3.operations import aio_client


@apm.trace()
async def get_document(key: str) -> str:
    key = f"{CI_COMMIT_REF_NAME}/documents/{key}"

    with io.BytesIO() as stream:

        # Stream the download to an in-memory buffer
        async with aio_client() as client:
            try:
                await client.download_fileobj(BUCKET_ANALYTICS, key, stream)
            except ClientError:
                raise DocumentNotFound()

        # Return pointer to begin-of-file
        stream.seek(0)

        # Documents are guaranteed to be UTF-8 encoded
        return stream.read().decode()


@apm.trace()
async def get_snapshot(key: str) -> bytes:
    key = f"{CI_COMMIT_REF_NAME}/snapshots/{key}"

    with io.BytesIO() as stream:

        # Stream the download to an in-memory buffer
        async with aio_client() as client:
            await client.download_fileobj(BUCKET_ANALYTICS, key, stream)

        # Return pointer to begin-of-file
        stream.seek(0)

        return stream.read()
