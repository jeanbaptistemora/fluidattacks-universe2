
import asyncio
import sys

from typing import Any, cast
import rollbar
from ariadne import (
    convert_kwargs_to_snake_case,
    convert_camel_case_to_snake
)
from asgiref.sync import sync_to_async

from backend.decorators import require_login, require_project_access
from backend.domain import (
    finding as finding_domain,
    project as project_domain,
    user as user_domain,
    vulnerability as vuln_domain
)
from backend.exceptions import (
    PermissionDenied, RequestedReportError,
)
from backend.reports import report
from backend.reports.reports import (
    data as data_report,
    technical as technical_report,
)
from backend.typing import (
    Report as ReportType,
    SimplePayload as SimplePayloadType
)
from backend import authz, util
from backend.utils import aio
from graphql.type.definition import GraphQLResolveInfo


@convert_kwargs_to_snake_case  # type: ignore
@require_login
async def resolve_report(
        _: Any,
        info: GraphQLResolveInfo,
        **parameters: str) -> ReportType:
    """Resolve report query."""
    return await resolve(info, **parameters)


@convert_kwargs_to_snake_case  # type: ignore
@require_login
@require_project_access
async def resolve_report_mutation(
        _: Any,
        info: GraphQLResolveInfo,
        **parameters: str) -> SimplePayloadType:
    """Resolve reports mutation."""
    return await _do_request_project_report(info, **parameters)


async def resolve(
        info: GraphQLResolveInfo,
        report_type: str,
        **parameters: str) -> ReportType:
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
        requested_field = convert_camel_case_to_snake(
            requested_field.name.value
        )
        if requested_field.startswith('_'):
            continue
        resolver_func = getattr(
            sys.modules[__name__],
            f'_get_{requested_field}'
        )
        result[requested_field] = resolver_func(info, **params)
    return result


async def _get_url_complete(info: GraphQLResolveInfo, user_email: str) -> str:
    projects = await user_domain.get_projects(user_email)
    url = await aio.ensure_io_bound(
        report.generate_complete_report,
        user_email, projects
    )
    util.cloudwatch_log(
        info.context,
        f'Security: Complete report succesfully requested by {user_email}'
    )
    return cast(str, url)


async def _get_url_all_vulns(
        info: GraphQLResolveInfo,
        user_email: str,
        project_name: str) -> str:
    if authz.get_user_level_role(user_email) == 'admin':
        url = await aio.ensure_io_bound(
            report.generate_all_vulns_report,
            user_email,
            project_name
        )
        msg = (
            'Security: All vulnerabilities report '
            f'successfully requested by {user_email}'
        )
        util.cloudwatch_log(info.context, msg)
    else:
        url = f'{user_email} is not allowed to perform this operation'
        msg = (
            f'Error: {user_email} is not allowed to '
            'request an all vulnerabilites report'
        )
        rollbar.report_message(msg, 'error')
        raise PermissionDenied()
    return cast(str, url)


async def _get_url_group_report(
    info: GraphQLResolveInfo,
    report_type: str,
    user_email: str,
    project_name: str,
    lang: str
) -> str:
    project_findings = await info.context.loaders['project'].load(project_name)
    project_findings = project_findings['findings']
    params = {
        'project_findings': project_findings,
        'context': info.context,
        'project_name': project_name,
        'lang': lang
    }
    try:
        url = await report.generate_group_report(
            report_type,
            user_email,
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
    return url


async def _get_url_all_users(
        info: GraphQLResolveInfo,
        user_email: str) -> str:
    if authz.get_user_level_role(user_email) == 'admin':
        url = await sync_to_async(
            report.generate_all_users_report)(
                user_email
        )
        msg = (
            f'Security: All users report successfully requested '
            f'by {user_email}'
        )
        util.cloudwatch_log(info.context, msg)
    else:
        url = f'{user_email} is not allowed to perform this operation'
        msg = (
            f'Error: {user_email} is not allowed to request an all'
            f'users report'
        )
        rollbar.report_message(msg, 'error')
        raise PermissionDenied()
    return cast(str, url)


async def _get_url(
        info: GraphQLResolveInfo,
        report_type: str,
        **parameters: str) -> str:
    url = ''
    user_info = util.get_jwt_content(info.context)
    user_email = user_info['user_email']
    project_name = parameters.get('project_name', '')
    if report_type == 'COMPLETE':
        url = await _get_url_complete(info, user_email)
    if report_type == 'ALL_USERS':
        url = await _get_url_all_users(info, user_email)
    if report_type == 'ALL_VULNS':
        url = await _get_url_all_vulns(info, user_email, project_name)
    elif report_type in ['PDF', 'XLS', 'DATA']:
        url = await _get_url_group_report(
            info,
            report_type,
            user_email,
            project_name,
            parameters.get('lang', 'en')
        )
    else:
        msg = f'Error: An error occurred getting the specified {report_type}'
        rollbar.report_message(msg, 'error')
    return url


async def _do_request_project_report(
        info: GraphQLResolveInfo,
        **parameters: str) -> SimplePayloadType:
    success = False
    project_name = parameters.get('project_name', '')
    project_name = project_name.lower()
    report_type = parameters.get('report_type')
    user_info = util.get_jwt_content(info.context)
    user_email = user_info['user_email']
    project_findings = await info.context.loaders['project'].load(project_name)
    project_findings = project_findings['findings']
    findings = await finding_domain.get_findings_async(project_findings)
    findings = [
        await sync_to_async(finding_domain.cast_new_vulnerabilities)(
            await vuln_domain.get_open_vuln_by_type(
                str(finding['findingId']), info.context
            ),
            finding
        )
        for finding in findings
    ]
    description = await sync_to_async(project_domain.get_description)(
        project_name.lower()
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
        util.cloudwatch_log(
            info.context,
            'Security: PDF report successfully requested'
        )
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
            'Security: XLS report successfully requested'
        )
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
            'Security: DATA report successfully requested'
        )

    return SimplePayloadType(success=success)
