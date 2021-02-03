# Standard library
import logging
from typing import Any, Dict, cast

# Third party libraries
from ariadne import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local libraries
from backend import authz, util
from backend.dal.helpers.redis import (
    redis_del_by_deps_soon,
)
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
    require_login
)
from backend.domain import (
    project as group_domain,
)
from backend.typing import (
    Invitation as InvitationType,
    EditStakeholderPayload as EditStakeholderPayloadType
)
from backend.utils import (
    user as user_utils,
)
from backend.utils.validations import validate_fluidattacks_staff_on_group

from back.settings import LOGGING


logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def _update_stakeholder(
    info: GraphQLResolveInfo,
    updated_data: Dict[str, str]
) -> bool:
    success = False
    group_name = updated_data['project_name'].lower()
    modified_role = updated_data['role']
    modified_email = updated_data['email']
    project_access = await group_domain.get_user_access(
        modified_email,
        group_name
    )
    invitation = cast(InvitationType, project_access.get('invitation'))
    if invitation and not invitation['is_used']:
        success = await user_utils.update_invited_stakeholder(
            updated_data,
            invitation,
            group_name
        )
    else:
        if await authz.grant_group_level_role(
            modified_email, group_name, modified_role
        ):
            success = await user_utils.modify_user_information(
                info.context, updated_data, group_name
            )
        else:
            LOGGER.error(
                'Couldn\'t update stakeholder role',
                extra={'extra': info.context}
            )

    return success


@convert_kwargs_to_snake_case  # type: ignore
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def mutate(
    _: Any,
    info: GraphQLResolveInfo,
    **updated_data: str
) -> EditStakeholderPayloadType:
    project_name = updated_data['project_name'].lower()
    modified_role = updated_data['role']
    modified_email = updated_data['email']

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
        success = await _update_stakeholder(info, updated_data)
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
        redis_del_by_deps_soon('edit_stakeholder', group_name=project_name)
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
            email=updated_data['email']
        )
    )
