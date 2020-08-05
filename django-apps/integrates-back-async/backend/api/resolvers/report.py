import logging
import sys

from typing import Any, cast
from ariadne import (
    convert_kwargs_to_snake_case,
    convert_camel_case_to_snake
)
from asgiref.sync import sync_to_async
from graphql.type.definition import GraphQLResolveInfo

from backend.decorators import require_login
from backend.domain import (
    user as user_domain,
)
from backend.exceptions import (
    PermissionDenied, RequestedReportError,
)
from backend.reports import report
from backend.typing import (
    Report as ReportType,
)
from backend import authz, util
from backend.utils import aio


# Constants
LOGGER = logging.getLogger(__name__)


@convert_kwargs_to_snake_case  # type: ignore
@require_login
async def resolve_report(
        _: Any,
        info: GraphQLResolveInfo,
        **parameters: str) -> ReportType:
    """Resolve report query."""
    return await resolve(info, **parameters)


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
    if await authz.get_user_level_role(user_email) == 'admin':
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
        msg = (
            f'Security: {user_email} is not allowed to '
            'request an all vulnerabilites report'
        )
        util.cloudwatch_log(info.context, msg)
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
    except RequestedReportError as ex:
        payload_data = {
            'report_type': report_type,
            'project_name': project_name,
            'user_email': user_email
        }
        LOGGER.exception(ex, extra={'extra': payload_data})
    return url


async def _get_url_all_users(
        info: GraphQLResolveInfo,
        user_email: str) -> str:
    if await authz.get_user_level_role(user_email) == 'admin':
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
        msg = (
            f'Security: {user_email} is not allowed to request an '
            'all users report'
        )
        util.cloudwatch_log(info.context, msg)
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
        payload_data = {
            'project_name': project_name,
            'report_type': report_type,
            'user_email': user_email
        }
        LOGGER.error(
            'Report type not in expected values',
            extra={'extra': payload_data})
    return url
