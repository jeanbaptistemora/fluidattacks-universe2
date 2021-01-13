# Standard library
import logging
from typing import Any

# Third party libraries
from ariadne import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local libraries
from backend import authz, util
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
    require_login
)
from backend.typing import (
    EditStakeholderPayload as EditStakeholderPayloadType
)
from backend.utils.user import modify_user_information
from backend.utils.validations import validate_fluidattacks_staff_on_group

from back.settings import LOGGING


logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


@convert_kwargs_to_snake_case  # type: ignore
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def mutate(
    _: Any,
    info: GraphQLResolveInfo,
    **modified_user_data: str
) -> EditStakeholderPayloadType:
    project_name = modified_user_data['project_name'].lower()
    modified_role = modified_user_data['role']
    modified_email = modified_user_data['email']

    success = False
    user_data = await util.get_jwt_content(info.context)
    user_email = user_data['user_email']

    allowed_roles_to_grant = \
        await authz.get_group_level_roles_a_user_can_grant(
            group=project_name,
            requester_email=user_email,
        )

    await validate_fluidattacks_staff_on_group(
        project_name, modified_email, modified_role
    )

    if modified_role in allowed_roles_to_grant:
        if await authz.grant_group_level_role(
                modified_email, project_name, modified_role):
            success = await modify_user_information(
                info.context, modified_user_data, project_name
            )
        else:
            LOGGER.error(
                'Couldn\'t update stakeholder role',
                extra={'extra': info.context}
            )
    else:
        LOGGER.error(
            'Invalid role provided',
            extra={
                'extra': {
                    'modified_user_role': modified_role,
                    'project_name': project_name,
                    'requester_email': user_email
                }
            })

    if success:
        util.queue_cache_invalidation(
            f'stakeholders*{project_name}',
            modified_email
        )
        msg = (
            f'Security: Modified stakeholder data: {modified_email} '
            f'in {project_name} project successfully'
        )
        util.cloudwatch_log(info.context, msg)
    else:
        msg = (
            f'Security: Attempted to modify stakeholder '
            f'data:{modified_email} in '
            f'{project_name} project'
        )
        util.cloudwatch_log(info.context, msg)

    return EditStakeholderPayloadType(
        success=success,
        modified_stakeholder=dict(
            project_name=project_name,
            email=modified_user_data['email']
        )
    )
