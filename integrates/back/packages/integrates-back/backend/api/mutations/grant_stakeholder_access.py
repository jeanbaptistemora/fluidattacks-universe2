# Standard library
import logging
from typing import Any

# Third party libraries
from aioextensions import (
    collect,
)
from ariadne import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local libraries
from back.settings import LOGGING

from backend import (
    authz,
    util
)
from backend.dal.helpers.redis import (
    redis_del_by_deps_soon,
)
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
    require_login
)
from backend.domain import user as user_domain
from backend.typing import (
    GrantStakeholderAccessPayload as GrantStakeholderAccessPayloadType,
)
from backend.utils.user import create_new_user
from backend.utils import (
    datetime as datetime_utils,
)
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
    role: str,
    **query_args: str
) -> GrantStakeholderAccessPayloadType:
    project_name = query_args.get('project_name', '').lower()
    success = False
    user_data = await util.get_jwt_content(info.context)
    user_email = user_data['user_email']
    new_user_role = role
    new_user_email = query_args.get('email', '')
    new_user_responsibility = query_args.get('responsibility', '-')
    invitation_date = datetime_utils.get_as_str(
        datetime_utils.get_now()
    )

    allowed_roles_to_grant = \
        await authz.get_group_level_roles_a_user_can_grant(
            group=project_name,
            requester_email=user_email,
        )

    if new_user_role in allowed_roles_to_grant:
        success = all(await collect([
            create_new_user(
                context=info.context,
                email=new_user_email,
                responsibility=new_user_responsibility,
                role=new_user_role,
                phone_number=query_args.get('phone_number', ''),
                group=project_name
            ),
            user_domain.update_project_access(
                new_user_email,
                project_name,
                False
            ),
            user_domain.update_project_responsibility(
                new_user_email,
                project_name,
                new_user_responsibility
            ),
            user_domain.update_project_invitation_date(
                new_user_email,
                project_name,
                invitation_date
            )
        ]))
    else:
        LOGGER.error(
            'Invalid role provided',
            extra={
                'extra': {
                    'new_user_role': new_user_role,
                    'project_name': project_name,
                    'requester_email': user_email
                }
            }
        )

    if success:
        organization_ids = await user_domain.get_organizations(new_user_email)
        redis_del_by_deps_soon(
            'grant_stakeholder_access',
            group_name=project_name,
        )
        util.queue_cache_invalidation(
            f'stakeholders*{project_name}',
            new_user_email,
            organization_ids[0]
        )
        util.cloudwatch_log(
            info.context,
            f'Security: Given grant access to {new_user_email} '
            f'in {project_name} project'
        )
    else:
        LOGGER.error(
            'Couldn\'t grant access to project',
            extra={'extra': info.context}
        )
        util.cloudwatch_log(
            info.context,
            f'Security: Attempted to grant access to {new_user_email} '
            f'in {project_name} project'
        )

    return GrantStakeholderAccessPayloadType(
        success=success,
        granted_stakeholder=dict(
            project_name=project_name,
            email=new_user_email
        )
    )
