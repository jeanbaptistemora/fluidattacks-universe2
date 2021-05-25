from typing import cast

from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

import authz
from custom_exceptions import (
    InvalidParameter,
    StakeholderNotFound,
)
from custom_types import Stakeholder
from decorators import (
    enforce_group_level_auth_async,
    enforce_organization_level_auth_async,
    require_login,
)
from group_access import domain as group_access_domain
from users import domain as stakeholders_domain


@enforce_organization_level_auth_async
async def _resolve_for_organization(
    _info: GraphQLResolveInfo,
    email: str,
    organization_id: str,
) -> Stakeholder:
    stakeholder: Stakeholder = await stakeholders_domain.get_by_email(email)
    org_role: str = await authz.get_organization_level_role(
        email, organization_id
    )
    if org_role:
        return {**stakeholder, "responsibility": "", "role": org_role}
    raise StakeholderNotFound()


@enforce_group_level_auth_async
async def _resolve_for_group(
    _info: GraphQLResolveInfo,
    email: str,
    group_name: str,
) -> Stakeholder:
    stakeholder: Stakeholder = await stakeholders_domain.get_by_email(email)
    group_role: str = await authz.get_group_level_role(email, group_name)

    if group_role:
        access = await group_access_domain.get_user_access(email, group_name)
        return {
            **stakeholder,
            "responsibility": cast(str, access.get("responsibility", "")),
            "role": group_role,
        }
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

    if entity == "PROJECT" and "project_name" in kwargs:
        group_name: str = kwargs["project_name"].lower()
        return await _resolve_for_group(
            info,
            email,
            group_name=group_name,
        )

    raise InvalidParameter()
