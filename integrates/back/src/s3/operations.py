from aioextensions import (
    in_thread,
)
from botocore.exceptions import (
    ClientError,
)
from custom_exceptions import (
    ErrorUploadingFileS3,
    UnavailabilityError,
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
from starlette.datastructures import (
    UploadFile,
)
from tempfile import (
    _TemporaryFileWrapper as TemporaryFileWrapper,
)
from typing import (
    Dict,
    List,
    Optional,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def download_file(bucket: str, file_name: str, file_path: str) -> None:
    client = await get_s3_resource()
    await client.download_file(bucket, file_name, file_path)


async def list_files(bucket: str, name: Optional[str] = None) -> List[str]:
    client = await get_s3_resource()
    resp = await client.list_objects_v2(Bucket=bucket, Prefix=name)

    return [item["Key"] for item in resp.get("Contents", [])]


async def remove_file(bucket: str, name: str) -> None:
    client = await get_s3_resource()
    try:
        response = await client.delete_object(Bucket=bucket, Key=name)
        status_code = response["ResponseMetadata"]["HTTPStatusCode"]
        if status_code not in [200, 204]:
            raise UnavailabilityError()
    except ClientError as ex:
        LOGGER.exception(ex, extra={"extra": locals()})
        raise UnavailabilityError() from ex


async def sign_url(file_name: str, expire_mins: float, bucket: str) -> str:
    client = await get_s3_resource()
    try:
        return str(
            await client.generate_presigned_url(
                ClientMethod="get_object",
                Params={"Bucket": bucket, "Key": file_name},
                ExpiresIn=expire_mins,
                HttpMethod="GET",
            )
        )
    except ClientError as ex:
        LOGGER.exception(ex, extra={"extra": locals()})
        raise UnavailabilityError() from ex


async def upload_memory_file(
    bucket: str, file_object: object, file_name: str
) -> None:
    valid_in_memory_files = (TemporaryFileWrapper, UploadFile)
    if not isinstance(file_object, valid_in_memory_files):
        LOGGER.error(
            "Attempt to upload invalid memory file", extra={"extra": locals()}
        )
        raise ErrorUploadingFileS3()

    bytes_object = io.BytesIO(await in_thread(file_object.file.read))
    client = await get_s3_resource()
    try:
        await client.upload_fileobj(
            bytes_object,
            bucket,
            file_name.lstrip("/"),
        )
    except ClientError as ex:
        LOGGER.exception(ex, extra={"extra": locals()})
        raise UnavailabilityError() from ex


async def sing_upload_url(
    file_name: str, expire_mins: float, bucket: str
) -> Dict[str, Dict[str, str]]:
    params = {
        "conditions": [
            {"acl": "private"},
            {"bucket": bucket},
            ["starts-with", "$key", file_name],
            ["content-length-range", 1, 5368709120],
        ]
    }

    client = await get_s3_resource()
    try:
        return await client.generate_presigned_post(
            bucket,
            file_name,
            Fields=None,
            Conditions=params["conditions"],
            ExpiresIn=expire_mins,
        )
    except ClientError as ex:
        LOGGER.exception(ex, extra={"extra": locals()})
        raise UnavailabilityError() from ex
