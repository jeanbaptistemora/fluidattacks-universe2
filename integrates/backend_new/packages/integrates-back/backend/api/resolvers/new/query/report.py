# Standard
import logging
from typing import Dict, List, Optional

# Third party
from aiodataloader import DataLoader
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import util
from backend.decorators import (
    enforce_group_level_auth_async,
    enforce_user_level_auth_async,
    require_login
)
from backend.domain import user as user_domain
from backend.exceptions import InvalidParameter, RequestedReportError
from backend.reports import report
from backend.typing import Report
from fluidintegrates.settings import LOGGING


logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger(__name__)


@enforce_user_level_auth_async
async def _get_url_all_users(info: GraphQLResolveInfo, user_email: str) -> str:
    util.cloudwatch_log(
        info.context,
        f'Security: All users report requested by {user_email}'
    )

    return await report.generate_all_users_report(user_email)


@enforce_user_level_auth_async
async def _get_url_all_vulns(
    info: GraphQLResolveInfo,
    user_email: str,
    group_name: str
) -> str:
    util.cloudwatch_log(
        info.context,
        f'Security: All vulnerabilities report requested by {user_email} '
        f'for group {group_name}'
    )

    return await report.generate_all_vulns_report(user_email, group_name)


async def _get_url_complete(info: GraphQLResolveInfo, user_email: str) -> str:
    groups: List[str] = await user_domain.get_projects(user_email)
    util.cloudwatch_log(
        info.context,
        f'Security: Complete report requested by {user_email}'
    )

    return await report.generate_complete_report(user_email, groups)


@enforce_group_level_auth_async
async def _get_url_group_report(
    info: GraphQLResolveInfo,
    lang: str,
    report_type: str,
    user_email: str,
    group_name: str
) -> str:
    group_findings_loader: DataLoader = info.context.loaders['group_findings']
    finding_ids: List[str] = [
        finding['id']
        for finding in await group_findings_loader.load(group_name)
    ]

    try:
        util.cloudwatch_log(
            info.context,
            f'Security: {report_type} report requested by {user_email} for '
            f'group {group_name}'
        )

        return await report.generate_group_report(
            report_type,
            user_email,
            context=info.context,
            lang=lang,
            project_findings=finding_ids,
            project_name=group_name,
        )
    except RequestedReportError as ex:
        LOGGER.exception(
            ex,
            extra={
                'extra': {
                    'report_type': report_type,
                    'project_name': group_name,
                    'user_email': user_email
                }
            }
        )

        raise ex


@convert_kwargs_to_snake_case
@require_login
async def resolve(
    _parent: None,
    info: GraphQLResolveInfo,
    **kwargs: str
) -> Report:
    user_info: Dict[str, str] = await util.get_jwt_content(info.context)
    user_email: str = user_info['user_email']

    group_name: Optional[str] = kwargs.get('project_name')
    lang: str = kwargs.get('lang', 'en')
    report_type: str = kwargs['report_type']

    if report_type == 'ALL_USERS':
        return {'url': await _get_url_all_users(info, user_email)}

    if report_type == 'ALL_VULNS' and group_name:
        return {'url': await _get_url_all_vulns(info, user_email, group_name)}

    if report_type == 'COMPLETE':
        return {'url': await _get_url_complete(info, user_email)}

    if report_type in {'DATA', 'PDF', 'XLS'} and group_name:
        return {
            'url': await _get_url_group_report(
                info,
                lang,
                report_type,
                user_email,
                group_name=group_name,
            )
        }

    LOGGER.error(
        'Report type not in expected values',
        extra={
            'extra': {
                'project_name': group_name,
                'report_type': report_type,
                'user_email': user_email
            }
        }
    )

    raise InvalidParameter()
