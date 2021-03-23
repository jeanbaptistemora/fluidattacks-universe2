# Standard libraries
import logging
from typing import (
    Dict,
)

# Third party libraries
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
from backend.typing import Report
from batch import dal as batch_dal
from back.settings import LOGGING


logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger(__name__)


@enforce_group_level_auth_async
async def _get_url_group_report(
    _info: GraphQLResolveInfo,
    report_type: str,
    user_email: str,
    group_name: str
) -> str:
    url: str = ''
    success: bool = await batch_dal.put_action(
        action_name='report',
        entity=group_name,
        subject=user_email,
        additional_info=report_type,
    )
    if success:
        url = f'The report will be sent to {user_email} shortly'
    else:
        raise RequestedReportError()

    return url


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
    report_type: str = kwargs['report_type']

    return {
        'url': await _get_url_group_report(
            info,
            report_type,
            user_email,
            group_name=group_name,
        )
    }
