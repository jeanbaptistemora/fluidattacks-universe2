from context import (
    FI_AWS_S3_REPORTS_BUCKET as VULNS_BUCKET,
)
from s3 import (
    operations as s3_ops,
)
from starlette.datastructures import (
    UploadFile,
)


async def sign_url(vuln_file_name: str) -> str:
    return await s3_ops.sign_url(vuln_file_name, 10, VULNS_BUCKET)


async def upload_file(vuln_file: UploadFile) -> str:
    file_path: str = vuln_file.filename
    file_name: str = file_path.split("/")[-1]
    await s3_ops.upload_memory_file(
        VULNS_BUCKET,
        vuln_file,
        file_name,
    )
    return file_name
