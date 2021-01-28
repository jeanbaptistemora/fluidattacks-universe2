# Standard
# None

# Third party
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import util
from backend.dal.helpers.redis import (
    redis_del_by_deps_soon,
)
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
    require_login
)
from backend.domain import finding as finding_domain
from backend.typing import ApproveDraftPayload


@convert_kwargs_to_snake_case  # type: ignore
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    draft_id: str
) -> ApproveDraftPayload:
    """Resolve approve_draft mutation."""
    user_info = await util.get_jwt_content(info.context)
    reviewer_email = user_info['user_email']
    group_name = await finding_domain.get_project(draft_id)

    success, release_date = await finding_domain.approve_draft(
        draft_id, reviewer_email
    )
    if success:
        redis_del_by_deps_soon(
            'approve_draft',
            finding_id=draft_id,
            group_name=group_name,
        )
        util.cloudwatch_log(
            info.context,
            f'Security: Approved draft in {group_name} group successfully'
        )
    else:
        util.cloudwatch_log(
            info.context,
            f'Security: Attempted to approve draft in {group_name} group'
        )
    return ApproveDraftPayload(release_date=release_date, success=success)
