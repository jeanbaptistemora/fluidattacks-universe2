# Standard library
from typing import Optional

# Third party libraries
from aioextensions import (
    collect,
    in_process,
)

# Local libraries
from backend.api import get_new_context
from backend.domain import (
    finding as finding_domain,
    project as project_domain,
    vulnerability as vuln_domain,
)
from backend.reports.reports import (
    data as data_report,
    technical as technical_report,
)
from backend import util


async def get_group_report_url(
    *,
    report_type: str,
    group_name: str,
    passphrase: str,
    user_email: str,
) -> Optional[str]:
    context = get_new_context()
    group_findings = await finding_domain.list_findings(
        context, [group_name]
    )
    findings = await finding_domain.get_findings_async(group_findings[0])
    format_vulns = await collect([
        vuln_domain.get_open_vuln_by_type(
            context,
            str(finding['findingId'])
        )
        for finding in findings
    ])
    format_findings = await collect([
        in_process(
            finding_domain.cast_new_vulnerabilities,
            format_vuln,
            finding
        )
        for finding, format_vuln in zip(findings, format_vulns)
    ])
    findings_ord = util.ord_asc_by_criticality(list(format_findings))
    description = await project_domain.get_description(group_name)

    if report_type == 'XLS':
        return await technical_report.generate_xls_file(
            context,
            findings_ord=findings_ord,
            passphrase=passphrase,
        )
    if report_type == 'PDF':
        return await technical_report.generate_pdf_file(
            description=description,
            findings_ord=findings_ord,
            group_name=group_name,
            lang='en',
            passphrase=passphrase,
            user_email=user_email,
        )
    if report_type == 'DATA':
        return await data_report.generate(
            context=context,
            findings_ord=findings_ord,
            group=group_name,
            group_description=description,
            passphrase=passphrase,
            requester_email=user_email,
        )

    return None
