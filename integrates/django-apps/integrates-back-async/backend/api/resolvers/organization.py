import sys
from typing import (
    Any,
)

from ariadne import (
    convert_kwargs_to_snake_case
)
from graphql.type.definition import GraphQLResolveInfo

from backend import util
from backend.decorators import (
    concurrent_decorators,
    enforce_organization_level_auth_async,
    require_login,
    require_organization_access
)
from backend.domain import (
    organization as org_domain,
)
from backend.typing import (
    SimplePayload as SimplePayloadType,
)


@concurrent_decorators(
    require_organization_access,
    enforce_organization_level_auth_async,
)
async def _do_update_organization_policies(
    _: Any,
    info: GraphQLResolveInfo,
    **parameters: Any
) -> SimplePayloadType:
    user_data = await util.get_jwt_content(info.context)
    user_email = user_data['user_email']

    organization_id = parameters.pop('organization_id')
    organization_name = parameters.pop('organization_name')
    success: bool = await org_domain.update_policies(
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
    return SimplePayloadType(success=success)


@convert_kwargs_to_snake_case  # type: ignore
@require_login
async def resolve_organization_mutation(
        obj: Any,
        info: GraphQLResolveInfo,
        **parameters: Any) -> Any:
    """Resolve Organization mutation """
    field = util.camelcase_to_snakecase(info.field_name)
    resolver_func = getattr(sys.modules[__name__], f'_do_{field}')
    return await resolver_func(obj, info, **parameters)
