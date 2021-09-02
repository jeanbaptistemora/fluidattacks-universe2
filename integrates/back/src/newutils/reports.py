from context import (
    FI_AWS_S3_REPORTS_BUCKET,
)
from custom_types import (
    Finding as FindingType,
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
    cast,
    Dict,
    List,
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
        FI_AWS_S3_REPORTS_BUCKET,
        uploaded_file,
        file_name,
    )
    return await sign_url(path=file_name, minutes=ttl)


def ord_asc_by_criticality(
    data: List[Dict[str, FindingType]]
) -> List[Dict[str, FindingType]]:
    """Sort the findings by criticality"""
    for i in range(0, len(data) - 1):
        for j in range(i + 1, len(data)):
            firstc = float(cast(float, data[i]["severityCvss"]))
            seconc = float(cast(float, data[j]["severityCvss"]))
            if firstc < seconc:
                aux = data[i]
                data[i] = data[j]
                data[j] = aux
    return data


# Default ttl for reports is 1 hour = 3600 seconds
async def sign_url(path: str, minutes: float = 3600) -> str:
    return await s3_ops.sign_url(path, minutes, FI_AWS_S3_REPORTS_BUCKET)


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
        FI_AWS_S3_REPORTS_BUCKET,
        report,
        file_name,
    )
    return file_name
