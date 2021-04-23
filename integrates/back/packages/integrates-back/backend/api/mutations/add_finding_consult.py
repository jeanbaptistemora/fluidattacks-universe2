# Standard libraries
from time import time
from typing import Any

# Third party libraries
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local libraries
from backend import util
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
    require_login
)
from backend.typing import AddConsultPayload as AddConsultPayloadType
from custom_exceptions import PermissionDenied
from findings import domain as findings_domain
from newutils import datetime as datetime_utils
from redis_cluster.operations import redis_del_by_deps_soon


@convert_kwargs_to_snake_case  # type: ignore
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def mutate(
    _: Any,
    info: GraphQLResolveInfo,
    **parameters: Any
) -> AddConsultPayloadType:
    success = False
    param_type = parameters.get('type', '').lower()
    user_data = await util.get_jwt_content(info.context)
    user_email = user_data['user_email']
    finding_id = str(parameters.get('finding_id'))
    finding_loader = info.context.loaders.finding
    finding = await finding_loader.load(finding_id)
    group = finding.get('project_name')
    content = parameters['content']

    user_email = user_data['user_email']
    comment_id = int(round(time() * 1000))
    current_time = datetime_utils.get_as_str(
        datetime_utils.get_now()
    )
    comment_data = {
        'user_id': comment_id,
        'comment_type': param_type if param_type != 'consult' else 'comment',
        'content': content,
        'fullname': ' '.join(
            [user_data['first_name'], user_data['last_name']]
        ),
        'parent': parameters.get('parent'),
        'created': current_time,
        'modified': current_time,
    }
    try:
        success = await findings_domain.add_comment(
            info,
            user_email,
            comment_data,
            finding_id,
            group
        )
    except PermissionDenied:
        util.cloudwatch_log(
            info.context,
            'Security: Unauthorized role attempted to add observation'
        )

    if success:
        redis_del_by_deps_soon('add_finding_consult', finding_id=finding_id)
        if content.strip() not in {'#external', '#internal'}:
            findings_domain.send_comment_mail(
                user_email,
                comment_data,
                finding
            )

        util.cloudwatch_log(
            info.context,
            f'Security: Added comment in finding {finding_id} successfully'
        )
    else:
        util.cloudwatch_log(
            info.context,
            f'Security: Attempted to add comment in finding {finding_id}'
        )

    return AddConsultPayloadType(success=success, comment_id=str(comment_id))
