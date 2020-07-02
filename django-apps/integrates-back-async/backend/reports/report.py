import asyncio
from asgiref.sync import sync_to_async
from backend.domain import (
    finding as finding_domain,
    project as project_domain,
    vulnerability as vuln_domain,
)
from backend.exceptions import RequestedReportError
from backend.reports import (
    data as data_report,
    technical as technical_report,
)
from backend import util


async def generate_group_report(
        report_type: str,
        user_email: str,
        **parameters) -> str:
    context = parameters.get('context')
    project_findings = parameters.get('project_findings', [])
    project_name = parameters.get('project_name')

    success = False
    url = ''

    findings = await finding_domain.get_findings_async(project_findings)
    findings = [
        await sync_to_async(finding_domain.cast_new_vulnerabilities)
        (await sync_to_async(vuln_domain.get_open_vuln_by_type)
         (finding['findingId'], context), finding)
        for finding in findings]
    description = \
        await sync_to_async(
            project_domain.get_description)(str(project_name).lower())
    findings_ord = util.ord_asc_by_criticality(findings)

    if report_type == 'PDF':
        asyncio.create_task(
            sync_to_async(technical_report.generate_pdf)(
                description=description,
                findings_ord=findings_ord,
                group_name=project_name,
                lang=parameters.get('lang', 'en'),
                user_email=user_email,
            )
        )
        success = True
    elif report_type == 'XLS':
        asyncio.create_task(
            sync_to_async(technical_report.generate_xls)(
                findings_ord=findings_ord,
                group_name=project_name,
                user_email=user_email,
            )
        )
        success = True
    elif report_type == 'DATA':
        asyncio.create_task(
            sync_to_async(data_report.generate)(
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
