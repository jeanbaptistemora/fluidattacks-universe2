from .report_types import (
    data as data_report,
    technical as technical_report,
)
from aioextensions import (
    collect,
    in_process,
)
from context import (
    FI_API_STATUS,
)
from dataloaders import (
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from findings import (
    domain as findings_domain,
)
from groups import (
    domain as groups_domain,
)
from newutils import (
    reports as reports_utils,
)
from typing import (
    Optional,
    Tuple,
)
from vulnerabilities import (
    domain as vulns_domain,
)


async def get_group_report_url(  # pylint: disable=too-many-return-statements
    *,
    report_type: str,
    group_name: str,
    passphrase: str,
    user_email: str,
) -> Optional[str]:
    loaders = get_new_context()
    if FI_API_STATUS == "migration":
        group_findings_new_loader = loaders.group_findings_new
        group_findings_new: Tuple[
            Finding, ...
        ] = await group_findings_new_loader.load(group_name)
        findings_ord_new = tuple(
            sorted(
                group_findings_new,
                key=lambda finding: findings_domain.get_severity_score_new(
                    finding.severity
                ),
            )
        )
        description = await groups_domain.get_description(group_name)

        if report_type == "XLS":
            return await technical_report.generate_xls_file_new(
                loaders,
                findings_ord=findings_ord_new,
                group_name=group_name,
                passphrase=passphrase,
            )
        if report_type == "PDF":
            return await technical_report.generate_pdf_file_new(
                loaders=loaders,
                description=description,
                findings_ord=findings_ord_new,
                group_name=group_name,
                lang="en",
                passphrase=passphrase,
                user_email=user_email,
            )
        if report_type == "DATA":
            return await data_report.generate_new(
                loaders=loaders,
                findings_ord=findings_ord_new,
                group=group_name,
                group_description=description,
                passphrase=passphrase,
                requester_email=user_email,
            )

    else:
        group_findings = await findings_domain.list_findings(
            loaders, [group_name]
        )
        findings = await findings_domain.get_findings_async(group_findings[0])
        format_vulns = await collect(
            [
                vulns_domain.get_open_vuln_by_type(
                    loaders, str(finding["findingId"])
                )
                for finding in findings
            ]
        )
        format_findings = await collect(
            [
                in_process(
                    findings_domain.cast_new_vulnerabilities,
                    format_vuln,
                    finding,
                )
                for finding, format_vuln in zip(findings, format_vulns)
            ]
        )
        findings_ord = reports_utils.ord_asc_by_criticality(
            list(format_findings)
        )
        description = await groups_domain.get_description(group_name)

        if report_type == "XLS":
            return await technical_report.generate_xls_file(
                loaders,
                findings_ord=findings_ord,
                group_name=group_name,
                passphrase=passphrase,
            )
        if report_type == "PDF":
            return await technical_report.generate_pdf_file(
                loaders=loaders,
                description=description,
                findings_ord=findings_ord,
                group_name=group_name,
                lang="en",
                passphrase=passphrase,
                user_email=user_email,
            )
        if report_type == "DATA":
            return await data_report.generate(
                loaders=loaders,
                findings_ord=findings_ord,
                group=group_name,
                group_description=description,
                passphrase=passphrase,
                requester_email=user_email,
            )
    return None
