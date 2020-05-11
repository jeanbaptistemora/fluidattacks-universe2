
import asyncio
from asgiref.sync import sync_to_async
from backend.decorators import require_login, require_project_access
from backend.domain import (
    finding as finding_domain, project as project_domain,
    report as report_domain, vulnerability as vuln_domain
)
from backend.typing import SimplePayload as SimplePayloadType
from backend import util

from ariadne import convert_kwargs_to_snake_case


@convert_kwargs_to_snake_case
@require_login
@require_project_access
async def resolve_report_mutation(_, info, **parameters):
    """Resolve reports mutation."""
    return await _do_request_project_report(info, **parameters)


async def _do_request_project_report(info, **parameters) -> SimplePayloadType:
    success = False
    project_name = parameters.get('project_name', '')
    project_name = project_name.lower()
    report_type = parameters.get('report_type')
    user_info = util.get_jwt_content(info.context)
    user_email = user_info['user_email']
    project_findings = \
        await info.context.loaders['project'].load(project_name)
    project_findings = project_findings['findings']
    findings = await finding_domain.get_findings_async(project_findings)
    findings = [
        await sync_to_async(finding_domain.cast_new_vulnerabilities)
        (await sync_to_async(vuln_domain.get_open_vuln_by_type)
         (finding['findingId'], info.context), finding)
        for finding in findings]
    description = \
        await sync_to_async(
            project_domain.get_description)(project_name.lower())

    findings_ord = util.ord_asc_by_criticality(findings)
    if report_type == 'PDF':
        asyncio.create_task(
            sync_to_async(report_domain.generate_pdf_report)(
                project_name, user_email, parameters.get('lang', 'en'),
                findings_ord, description
            )
        )
        success = True
        util.cloudwatch_log(
            info.context,
            'Security: PDF report successfully requested')
    elif report_type == 'XLS':
        asyncio.create_task(
            sync_to_async(report_domain.generate_xls_report)(
                project_name, user_email, findings_ord
            )
        )
        success = True
        util.cloudwatch_log(
            info.context,
            'Security: XLS report successfully requested')

    return SimplePayloadType(success=success)
