# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from botocore.exceptions import (
    ClientError,
)
from custom_exceptions import (
    UnavailabilityError,
)
import json
from s3.resource import (
    get_s3_resource,
    s3_shutdown,
)
from typing import (
    Any,
    Dict,
)
from utils.logs import (
    log_blocking,
)


async def download_file(bucket: str, file_name: str, file_path: str) -> None:
    client = await get_s3_resource()
    await client.download_file(bucket, file_name, file_path)
    await s3_shutdown()


async def upload_object(
    file_name: str, dict_object: Dict[str, Any], bucket: str
) -> None:
    try:
        client = await get_s3_resource()
        await client.put_object(
            Body=json.dumps(dict_object, indent=2, sort_keys=True),
            Bucket=bucket,
            Key=file_name,
        )
    except ClientError as ex:
        log_blocking("error", "%s", ex)
        raise UnavailabilityError() from ex
    finally:
        await s3_shutdown()
