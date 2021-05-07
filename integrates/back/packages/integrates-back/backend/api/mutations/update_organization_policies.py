# Standard
from typing import Any

# Third party
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import util
from backend.typing import SimplePayload
from decorators import enforce_organization_level_auth_async
from organizations import domain as orgs_domain


@convert_kwargs_to_snake_case
@enforce_organization_level_auth_async
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    **parameters: Any
) -> SimplePayload:
    user_data = await util.get_jwt_content(info.context)
    user_email = user_data['user_email']

    organization_id = parameters.pop('organization_id')
    organization_name = parameters.pop('organization_name')
    success: bool = await orgs_domain.update_policies(
        info.context.loaders,
        organization_id,
        organization_name,
        user_email,
        parameters
    )
    if success:
        util.cloudwatch_log(
            info.context,
            f'Security: User {user_email} updated policies for organization '
            f'{organization_name} with ID {organization_id}'
        )
    return SimplePayload(success=success)
