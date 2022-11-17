# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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


@enforce_organization_level_auth_async
async def _resolve_for_organization(
    info: GraphQLResolveInfo,
    email: str,
    organization_id: str,
) -> Stakeholder:
    if not organization_id:
        raise StakeholderNotFound()
    loaders: Dataloaders = info.context.loaders
    return await loaders.stakeholder.load(email)


@enforce_group_level_auth_async
async def _resolve_for_group(
    info: GraphQLResolveInfo,
    email: str,
    group_name: str,
) -> Stakeholder:
    if not group_name:
        raise StakeholderNotFound()
    loaders: Dataloaders = info.context.loaders
    return await loaders.stakeholder.load(email)


@convert_kwargs_to_snake_case
@require_login
async def resolve(
    _parent: None, info: GraphQLResolveInfo, **kwargs: str
) -> Stakeholder:
    request_store = sessions_domain.get_request_store(info.context)
    entity: str = kwargs["entity"]
    request_store["entity"] = entity
    email: str = kwargs["user_email"]

    if entity == "ORGANIZATION" and "organization_id" in kwargs:
        org_id: str = kwargs["organization_id"]
        request_store["organization_id"] = org_id
        return await _resolve_for_organization(
            info,
            email,
            organization_id=org_id,
        )

    if entity == "GROUP" and "group_name" in kwargs:
        group_name: str = kwargs["group_name"]
        request_store["group_name"] = group_name
        return await _resolve_for_group(
            info,
            email,
            group_name=group_name,
        )

    raise InvalidParameter()
