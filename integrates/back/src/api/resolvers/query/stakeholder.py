from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
import authz
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
from group_access import (
    domain as group_access_domain,
)
from newutils.utils import (
    get_key_or_fallback,
)


@enforce_organization_level_auth_async
async def _resolve_for_organization(
    info: GraphQLResolveInfo,
    email: str,
    organization_id: str,
) -> Stakeholder:
    loaders: Dataloaders = info.context.loaders
    stakeholder: Stakeholder = await loaders.stakeholder.load(email)
    org_role: str = await authz.get_organization_level_role(
        email, organization_id
    )
    if org_role:
        stakeholder = stakeholder._replace(
            role=org_role,
        )
        return stakeholder
    raise StakeholderNotFound()


@enforce_group_level_auth_async
async def _resolve_for_group(
    info: GraphQLResolveInfo,
    email: str,
    group_name: str,
) -> Stakeholder:
    loaders: Dataloaders = info.context.loaders
    stakeholder: Stakeholder = await loaders.stakeholder.load(email)
    group_role: str = await authz.get_group_level_role(email, group_name)

    if group_role:
        access = await group_access_domain.get_user_access(email, group_name)
        stakeholder = stakeholder._replace(
            responsibility=access.get("responsibility", None),
            role=group_role,
        )
        return stakeholder
    raise StakeholderNotFound()


@convert_kwargs_to_snake_case
@require_login
async def resolve(
    _parent: None, info: GraphQLResolveInfo, **kwargs: str
) -> Stakeholder:
    entity: str = kwargs["entity"]
    email: str = kwargs["user_email"]

    if entity == "ORGANIZATION" and "organization_id" in kwargs:
        org_id: str = kwargs["organization_id"]
        return await _resolve_for_organization(
            info,
            email,
            organization_id=org_id,
        )

    if entity == "GROUP" and "group_name" in kwargs:
        group_name: str = get_key_or_fallback(kwargs)
        return await _resolve_for_group(
            info,
            email,
            group_name=group_name,
        )

    raise InvalidParameter()
