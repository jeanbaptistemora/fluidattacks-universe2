# Standard libraries
import logging
from typing import (
    cast,
    Dict,
    List
)

# Third party libraries
from aiodataloader import DataLoader
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local libraries
from backend import util
from backend.decorators import (
    enforce_group_level_auth_async,
    require_login
)
from backend.exceptions import (
    RequestedReportError
)
from backend.reports import report
from backend.typing import Report
from back.settings import LOGGING


logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger(__name__)


@enforce_group_level_auth_async
async def _get_url_group_report(
    info: GraphQLResolveInfo,
    lang: str,
    report_type: str,
    user_email: str,
    group_name: str
) -> str:
    group_findings_loader: DataLoader = info.context.loaders.group_findings
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

        return cast(
            str,
            await report.generate_group_report(
                report_type,
                user_email,
                context=info.context,
                lang=lang,
                project_findings=finding_ids,
                project_name=group_name,
            )
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


@convert_kwargs_to_snake_case  # type: ignore
@require_login
async def resolve(
    _parent: None,
    info: GraphQLResolveInfo,
    **kwargs: str
) -> Report:
    user_info: Dict[str, str] = await util.get_jwt_content(info.context)
    user_email: str = user_info['user_email']

    group_name: str = kwargs['project_name']
    lang: str = kwargs.get('lang', 'en')
    report_type: str = kwargs['report_type']

    return {
        'url': await _get_url_group_report(
            info,
            lang,
            report_type,
            user_email,
            group_name=group_name,
        )
    }
