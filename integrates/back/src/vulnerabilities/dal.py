from context import (
    FI_AWS_S3_REPORTS_BUCKET as VULNS_BUCKET,
)
import db_model.vulnerabilities as vulns_model
from db_model.vulnerabilities.types import (
    VulnerabilityVerification,
    VulnerabilityZeroRisk,
)
from s3 import (
    operations as s3_ops,
)
from starlette.datastructures import (
    UploadFile,
)
from typing import (
    Optional,
    Tuple,
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


async def update_verification(
    *,
    current_value: Optional[VulnerabilityVerification],
    finding_id: str,
    vulnerability_id: str,
    verification: VulnerabilityVerification,
) -> None:
    await vulns_model.update_historic_entry(
        current_entry=current_value,
        entry=verification,
        finding_id=finding_id,
        vulnerability_id=vulnerability_id,
    )


async def update_historic_verification(
    *,
    finding_id: str,
    vulnerability_id: str,
    historic_verification: Tuple[VulnerabilityVerification, ...],
) -> None:
    await vulns_model.update_historic(
        finding_id=finding_id,
        historic=historic_verification,
        vulnerability_id=vulnerability_id,
    )


async def update_zero_risk(
    *,
    current_value: Optional[VulnerabilityZeroRisk],
    finding_id: str,
    vulnerability_id: str,
    zero_risk: VulnerabilityZeroRisk,
) -> None:
    await vulns_model.update_historic_entry(
        current_entry=current_value,
        entry=zero_risk,
        finding_id=finding_id,
        vulnerability_id=vulnerability_id,
    )


async def update_historic_zero_risk(
    *,
    finding_id: str,
    vulnerability_id: str,
    historic_zero_risk: Tuple[VulnerabilityZeroRisk, ...],
) -> None:
    await vulns_model.update_historic(
        finding_id=finding_id,
        historic=historic_zero_risk,
        vulnerability_id=vulnerability_id,
    )
