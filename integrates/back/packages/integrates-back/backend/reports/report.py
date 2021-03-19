# Standard library
from typing import Any, Optional

# Third party libraries
from aioextensions import (
    collect,
    in_process,
    schedule,
)

# Local libraries
from backend.api import get_new_context
from backend.domain import (
    finding as finding_domain,
    project as project_domain,
    vulnerability as vuln_domain,
)
from backend.exceptions import RequestedReportError
from backend.reports.reports import (
    data as data_report,
    technical as technical_report,
)
from backend import util
from batch import dal as batch_dal
from newutils.reports import patch_loop_exception_handler


async def generate_group_report(
    report_type: str,
    user_email: str,
    **parameters: Any
) -> str:
    context = parameters['context']
    project_findings = parameters.get('project_findings', [])
    project_name = str(parameters.get('project_name'))

    success = False
    url = ''

    findings = await finding_domain.get_findings_async(project_findings)
    findings = [
        await in_process(
            finding_domain.cast_new_vulnerabilities,
            await vuln_domain.get_open_vuln_by_type(
                context,
                str(finding['findingId'])
            ),
            finding
        )
        for finding in findings
    ]
    description = await project_domain.get_description(
        str(project_name).lower()
    )
    findings_ord = util.ord_asc_by_criticality(findings)

    patch_loop_exception_handler(user_email, project_name, report_type)
    if report_type == 'PDF':
        schedule(
            technical_report.generate_pdf(
                description=description,
                findings_ord=findings_ord,
                group_name=project_name,
                lang=parameters.get('lang', 'en'),
                user_email=user_email,
            )
        )
        success = True
    elif report_type == 'XLS':
        success = await batch_dal.put_action(
            action_name='report',
            entity=project_name,
            subject=user_email,
            additional_info=report_type,
        )
    elif report_type == 'DATA':
        schedule(
            data_report.generate(
                context=context,
                findings_ord=findings_ord,
                group=project_name,
                group_description=description,
                requester_email=user_email,
            )
        )
        success = True
    if success:
        url = f'The report will be sent to {user_email} shortly'
    else:
        raise RequestedReportError()

    return url


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

    return None
