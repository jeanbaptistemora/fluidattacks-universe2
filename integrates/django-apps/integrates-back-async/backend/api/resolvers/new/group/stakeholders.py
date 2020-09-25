# Standard
from typing import cast, Dict, List

# Third party
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import authz
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates
)
from backend.domain import project as group_domain, user as stakeholder_domain
from backend.typing import Project as Group, Stakeholder
from backend.utils import aio


async def _get_stakeholder(email: str, group_name: str) -> Stakeholder:
    stakeholder: Stakeholder = await stakeholder_domain.get_by_email(email)
    group_role: str = await authz.get_group_level_role(email, group_name)
    access: Dict[str, str] = await group_domain.get_user_access(
        email,
        group_name
    )

    return {
        **stakeholder,
        'responsibility': access.get('responsibility', ''),
        'role': group_role
    }


@concurrent_decorators(
    enforce_group_level_auth_async,
    require_integrates,
)
async def resolve(
    parent: Group,
    _info: GraphQLResolveInfo,
    **_kwargs: None
) -> List[Stakeholder]:
    group_name: str = cast(str, parent['name'])

    group_stakeholders: List[str] = await group_domain.get_users(group_name)

    stakeholders: List[Stakeholder] = cast(
        List[Stakeholder],
        await aio.materialize(
            _get_stakeholder(email, group_name)
            for email in group_stakeholders
        )
    )

    return stakeholders
