# Standard library
import time
from typing import Any

# Third party libraries
from aioextensions import schedule
from ariadne import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local libraries
from backend import util
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
    require_integrates,
)
from backend.typing import AddConsultPayload as AddConsultPayloadType
from group_comments import domain as group_comments_domain
from mailer import groups as groups_mail
from newutils import datetime as datetime_utils
from redis_cluster.operations import redis_del_by_deps_soon


@convert_kwargs_to_snake_case  # type: ignore
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates
)
async def mutate(  # pylint: disable=too-many-arguments
    _: Any,
    info: GraphQLResolveInfo,
    **parameters: Any
) -> AddConsultPayloadType:
    group_name = parameters.get('project_name', '').lower()
    user_info = await util.get_jwt_content(info.context)
    user_email = user_info['user_email']
    current_time = datetime_utils.get_as_str(
        datetime_utils.get_now()
    )
    comment_id = int(round(time.time() * 1000))
    content = parameters['content']
    comment_data = {
        'user_id': comment_id,
        'content': content,
        'created': current_time,
        'fullname': str.join(
            ' ',
            [user_info['first_name'], user_info['last_name']]
        ),
        'modified': current_time,
        'parent': parameters.get('parent')
    }
    success = await group_comments_domain.add_comment(
        info,
        group_name,
        user_email,
        comment_data
    )
    if success:
        redis_del_by_deps_soon('add_group_consult', group_name=group_name)
        if content.strip() not in {'#external', '#internal'}:
            schedule(
                groups_mail.send_mail_comment(
                    info.context,
                    comment_data,
                    user_email,
                    group_name

                )
            )

        util.cloudwatch_log(
            info.context,
            f'Security: Added comment to {group_name} project successfully'
        )
    else:
        util.cloudwatch_log(
            info.context,
            f'Security: Attempted to add comment in {group_name} project'
        )

    return AddConsultPayloadType(success=success, comment_id=str(comment_id))
