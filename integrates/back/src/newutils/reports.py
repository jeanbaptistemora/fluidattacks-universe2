# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from context import (
    FI_AWS_S3_MAIN_BUCKET,
)
import logging
from s3 import (
    operations as s3_ops,
)
from starlette.datastructures import (
    UploadFile,
)
from typing import (
    Any,
)
from uuid import (
    uuid4 as uuid,
)

# Constants
LOGGER = logging.getLogger(__name__)


async def expose_bytes_as_url(
    *,
    content: bytes,
    ext: str = "",
    ttl: float,
) -> str:
    file_name: str = uuid().hex
    if ext:
        file_name += "." + ext

    uploaded_file = UploadFile(filename=file_name)
    await uploaded_file.write(content)
    await uploaded_file.seek(0)
    await s3_ops.upload_memory_file(
        FI_AWS_S3_MAIN_BUCKET,
        uploaded_file,
        f"reports/{file_name}",
    )
    return await sign_url(path=file_name, seconds=ttl)


# Default ttl for reports is 1 hour = 3600 seconds
async def sign_url(path: str, seconds: float = 3600) -> str:
    return await s3_ops.sign_url(
        f"reports/{path}", seconds, FI_AWS_S3_MAIN_BUCKET
    )


async def upload_report(file_name: str) -> str:
    with open(file_name, "rb") as file:
        uploaded_file = UploadFile(filename=file_name)
        await uploaded_file.write(file.read())
        await uploaded_file.seek(0)
        success = await upload_report_from_file_descriptor(uploaded_file)
        return success


async def upload_report_from_file_descriptor(report: Any) -> str:
    file_path = report.filename
    file_name: str = file_path.split("_")[-1]
    await s3_ops.upload_memory_file(
        FI_AWS_S3_MAIN_BUCKET,
        report,
        f"reports/{file_name}",
    )
    return file_name


def get_ordinal_ending(number: int) -> str:
    """
    Get the ordinal representation ending of an integer::

        get_ordinal_ending(22)   => "nd"
    """
    if 11 <= (number % 100) <= 13:
        return "th"
    return ["th", "st", "nd", "rd", "th"][min(number % 10, 4)]
