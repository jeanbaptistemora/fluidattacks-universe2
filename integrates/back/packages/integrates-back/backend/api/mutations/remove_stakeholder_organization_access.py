
# Standard
# None

# Third party
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import util
from backend.decorators import enforce_organization_level_auth_async
from backend.domain import organization as org_domain
from backend.typing import SimplePayload


@convert_kwargs_to_snake_case
@enforce_organization_level_auth_async
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    organization_id: str,
    user_email: str
) -> SimplePayload:
    user_data = await util.get_jwt_content(info.context)
    requester_email = user_data['user_email']
    organization_name = await org_domain.get_name_by_id(organization_id)

    success: bool = await org_domain.remove_user(
        organization_id, user_email.lower()
    )
    if success:
        util.queue_cache_invalidation(
            user_email,
            f'stakeholders*{organization_id.lower()}',
        )
        util.cloudwatch_log(
            info.context,
            f'Security: Stakeholder {requester_email} removed stakeholder'
            f' {user_email} from organization {organization_name}'
        )
    else:
        util.cloudwatch_log(
            info.context,
            f'Security: Stakeholder {requester_email} attempted to remove '
            f'stakeholder {user_email} from organization {organization_name}'
        )

    return SimplePayload(success=success)
