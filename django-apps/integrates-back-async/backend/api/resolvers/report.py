
import asyncio
import sys
import rollbar
from asgiref.sync import sync_to_async
from backend.decorators import require_login, require_project_access
from backend.domain import (
    finding as finding_domain, project as project_domain,
    user as user_domain, vulnerability as vuln_domain
)
from backend.exceptions import RequestedReportError
from backend.reports import (
    complete as complete_report,
    data as data_report,
    report,
    technical as technical_report,
)
from backend.typing import (
    Report as ReportType,
    SimplePayload as SimplePayloadType
)
from backend import util

from ariadne import convert_kwargs_to_snake_case, convert_camel_case_to_snake


@convert_kwargs_to_snake_case
@require_login
async def resolve_report(_, info, **parameters) -> ReportType:
    """Resolve report query."""
    return await resolve(info, **parameters)


@convert_kwargs_to_snake_case
@require_login
@require_project_access
async def resolve_report_mutation(_, info, **parameters):
    """Resolve reports mutation."""
    return await _do_request_project_report(info, **parameters)


async def resolve(info, report_type: str, **parameters) -> ReportType:
    """Async resolve fields."""
    result: ReportType = dict()
    for requested_field in info.field_nodes[0].selection_set.selections:
        if util.is_skippable(info, requested_field):
            continue
        params = {
            'report_type': report_type,
            **parameters
        }
        field_params = util.get_field_parameters(requested_field)
        if field_params:
            params.update(field_params)
        requested_field = \
            convert_camel_case_to_snake(requested_field.name.value)
        if requested_field.startswith('_'):
            continue
        resolver_func = getattr(
            sys.modules[__name__],
            f'_get_{requested_field}'
        )
        result[requested_field] = resolver_func(info, **params)
    return result


async def _get_url(info, report_type: str, **parameters) -> str:
    url = ''
    user_email = parameters.get('user_email')
    if report_type == 'COMPLETE':
        projects = await user_domain.get_projects(user_email)
        url = \
            await sync_to_async(
                complete_report.generate)(projects, user_email)
        util.cloudwatch_log(
            info.context,
            f'Security: Complete report succesfully requested by {user_email}')
    elif report_type in ['PDF', 'XLS', 'DATA']:
        project_name = parameters.get('project_name')
        project_findings = \
            await info.context.loaders['project'].load(project_name)
        project_findings = project_findings['findings']
        params = {
            'project_findings': project_findings,
            'context': info.context,
            'project_name': project_name,
        }
        try:
            url = await report.generate_group_report(
                report_type,
                str(user_email),
                **params
            )
            msg = (
                f'Security: {report_type} report successfully requested '
                f'by {user_email} in project {project_name}'
            )
            util.cloudwatch_log(info.context, msg)
        except RequestedReportError:
            msg = (
                f'Error: An error occurred getting the specified'
                f'{report_type} for proyect {project_name} by {user_email}'
            )
            rollbar.report_message(msg, 'error')
    else:
        msg = f'Error: An error occurred getting the specified {report_type}'
        rollbar.report_message(msg, 'error')
    return url


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
            sync_to_async(technical_report.generate_pdf)(
                description=description,
                findings_ord=findings_ord,
                group_name=project_name,
                lang=parameters.get('lang', 'en'),
                user_email=user_email,
            )
        )
        success = True
        util.cloudwatch_log(
            info.context,
            'Security: PDF report successfully requested')
    elif report_type == 'XLS':
        asyncio.create_task(
            sync_to_async(technical_report.generate_xls)(
                findings_ord=findings_ord,
                group_name=project_name,
                user_email=user_email,
            )
        )
        success = True
        util.cloudwatch_log(
            info.context,
            'Security: XLS report successfully requested')
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
        util.cloudwatch_log(
            info.context,
            'Security: DATA report successfully requested')

    return SimplePayloadType(success=success)
