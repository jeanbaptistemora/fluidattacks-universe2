from .report_types import (
    certificate as cert_report,
    data as data_report,
    technical as technical_report,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.findings.types import (
    Finding,
)
from db_model.groups.types import (
    Group,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
    VulnerabilityVerificationStatus,
)
from decimal import (
    Decimal,
)
from findings import (
    domain as findings_domain,
)
from typing import (
    Optional,
    Tuple,
)


async def get_group_report_url(  # pylint: disable=too-many-locals
    *,
    report_type: str,
    group_name: str,
    user_email: str,
    treatments: set[VulnerabilityTreatmentStatus],
    states: set[VulnerabilityStateStatus],
    verifications: set[VulnerabilityVerificationStatus],
    closing_date: Optional[datetime],
    finding_title: str,
    age: Optional[int],
    min_severity: Optional[Decimal],
    max_severity: Optional[Decimal],
) -> Optional[str]:
    loaders: Dataloaders = get_new_context()
    group_findings_loader = loaders.group_findings
    group_findings: Tuple[Finding, ...] = await group_findings_loader.load(
        group_name
    )
    findings_ord = tuple(
        sorted(
            group_findings,
            key=lambda finding: findings_domain.get_severity_score(
                finding.severity
            ),
            reverse=True,
        )
    )
    group: Group = await loaders.group.load(group_name)

    if report_type == "XLS":
        return await technical_report.generate_xls_file(
            loaders=loaders,
            findings_ord=findings_ord,
            group_name=group_name,
            treatments=treatments,
            states=states,
            verifications=verifications,
            closing_date=closing_date,
            finding_title=finding_title,
            age=age,
            min_severity=min_severity,
            max_severity=max_severity,
        )
    if report_type == "PDF":
        return await technical_report.generate_pdf_file(
            loaders=loaders,
            description=group.description,
            findings_ord=findings_ord,
            group_name=group_name,
            lang="en",
            user_email=user_email,
        )
    if report_type == "CERT":
        return await cert_report.generate_cert_file(
            loaders=loaders,
            description=group.description,
            findings_ord=findings_ord,
            group_name=group_name,
            lang=str(group.language.value).lower(),
            user_email=user_email,
        )
    if report_type == "DATA":
        return await data_report.generate(
            loaders=loaders,
            findings_ord=findings_ord,
            group=group_name,
            group_description=group.description,
            requester_email=user_email,
        )

    return None
