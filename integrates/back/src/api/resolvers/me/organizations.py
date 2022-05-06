from aioextensions import (
    collect,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    organizations as orgs_utils,
)
from organizations import (
    domain as orgs_domain,
)
from typing import (
    Any,
)


async def resolve(
    parent: dict[str, Any],
    _info: GraphQLResolveInfo,
    **_kwargs: None,
) -> tuple[dict[str, Any], ...]:
    user_email = str(parent["user_email"])
    organization_ids: list[str] = await orgs_domain.get_user_organizations(
        user_email
    )
    organizations = await collect(
        tuple(orgs_domain.get_by_id(id) for id in organization_ids)
    )

    return orgs_utils.filter_active_organizations(organizations)
