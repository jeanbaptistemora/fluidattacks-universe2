import asyncio
from typing import List
from asgiref.sync import sync_to_async
from backend.domain import (
    finding as finding_domain,
    project as project_domain,
    vulnerability as vuln_domain,
)
from backend.exceptions import RequestedReportError
from backend.reports.reports import (
    complete as complete_report,
    data as data_report,
    technical as technical_report,
    all_users as all_users_report,
    all_vulns as all_vulns_report,
)
from backend import util


async def generate_group_report(
    report_type: str,
    user_email: str,
    **parameters
) -> str:
    context = parameters.get('context')
    project_findings = parameters.get('project_findings', [])
    project_name = parameters.get('project_name')

    success = False
    url = ''

    findings = await finding_domain.get_findings_async(project_findings)
    findings = [
        await sync_to_async(finding_domain.cast_new_vulnerabilities)
        (await vuln_domain.get_open_vuln_by_type(
            str(finding['findingId']), context), finding)
        for finding in findings]
    description = await project_domain.get_description(
        str(project_name).lower()
    )
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


def generate_complete_report(user_email: str, projects: List[str]) -> str:
    return complete_report.generate(user_email, projects)


def generate_all_vulns_report(user_email: str, project_name: str = '') -> str:
    return all_vulns_report.generate(user_email, project_name)


def generate_all_users_report(user_email: str) -> str:
    return all_users_report.generate(user_email)
