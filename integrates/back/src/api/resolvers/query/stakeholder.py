from .schema import (
    QUERY,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    InvalidParameter,
    StakeholderNotFound,
)
from dataloaders import (
    Dataloaders,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from decorators import (
    enforce_group_level_auth_async,
    enforce_organization_level_auth_async,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from sessions import (
    domain as sessions_domain,
)
from stakeholders.domain import (
    get_stakeholder,
)


@enforce_organization_level_auth_async
async def _resolve_for_organization(
    *,
    info: GraphQLResolveInfo,
    email: str,
    organization_id: str,
    user_email: str,
) -> Stakeholder:
    if not organization_id:
        raise StakeholderNotFound()
    loaders: Dataloaders = info.context.loaders
    return await get_stakeholder(loaders, email, user_email)


@enforce_group_level_auth_async
async def _resolve_for_group(
    *,
    info: GraphQLResolveInfo,
    email: str,
    group_name: str,
    user_email: str,
) -> Stakeholder:
    if not group_name:
        raise StakeholderNotFound()
    loaders: Dataloaders = info.context.loaders
    return await get_stakeholder(loaders, email, user_email)


@QUERY.field("stakeholder")
@convert_kwargs_to_snake_case
@require_login
async def resolve(
    _parent: None, info: GraphQLResolveInfo, **kwargs: str
) -> Stakeholder:
    request_store = sessions_domain.get_request_store(info.context)
    entity: str = kwargs["entity"]
    request_store["entity"] = entity
    email: str = kwargs["user_email"]
    user_data = await sessions_domain.get_jwt_content(info.context)
    user_email: str = user_data["user_email"]

    if entity == "ORGANIZATION" and "organization_id" in kwargs:
        org_id: str = kwargs["organization_id"]
        request_store["organization_id"] = org_id
        return await _resolve_for_organization(
            info=info,
            email=email,
            organization_id=org_id,
            user_email=user_email,
        )

    if entity == "GROUP" and "group_name" in kwargs:
        group_name: str = kwargs["group_name"]
        request_store["group_name"] = group_name
        return await _resolve_for_group(
            info=info,
            email=email,
            group_name=group_name,
            user_email=user_email,
        )

    raise InvalidParameter()
