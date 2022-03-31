from .report_types import (
    certificate as cert_report,
    data as data_report,
    technical as technical_report,
)
from dataloaders import (
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from db_model.groups.types import (
    Group,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityTreatmentStatus,
)
from findings import (
    domain as findings_domain,
)
from typing import (
    Optional,
    Set,
    Tuple,
)


async def get_group_report_url(
    *,
    report_type: str,
    group_name: str,
    passphrase: str,
    user_email: str,
    treatments: Set[VulnerabilityTreatmentStatus],
) -> Optional[str]:
    loaders = get_new_context()
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
    group: Group = await loaders.group_typed.load(group_name)

    if report_type == "XLS":
        return await technical_report.generate_xls_file(
            loaders,
            findings_ord=findings_ord,
            group_name=group_name,
            passphrase=passphrase,
            treatments=treatments,
        )
    if report_type == "PDF":
        return await technical_report.generate_pdf_file(
            loaders=loaders,
            description=group.description,
            findings_ord=findings_ord,
            group_name=group_name,
            lang="en",
            passphrase=passphrase,
            user_email=user_email,
        )
    if report_type == "CERT":
        return await cert_report.generate_cert_file(
            loaders=loaders,
            description=group.description,
            findings_ord=findings_ord,
            group_name=group_name,
            lang=str(group.language.value).lower(),
        )
    if report_type == "DATA":
        return await data_report.generate(
            loaders=loaders,
            findings_ord=findings_ord,
            group=group_name,
            group_description=group.description,
            passphrase=passphrase,
            requester_email=user_email,
        )

    return None
