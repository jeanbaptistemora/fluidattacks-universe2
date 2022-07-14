from db_model.stakeholders.types import (
    Stakeholder,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from group_access import (
    domain as group_access_domain,
)
from newutils import (
    token as token_utils,
)
from organizations import (
    domain as orgs_domain,
)
from typing import (
    Optional,
)


async def resolve(
    parent: Stakeholder,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Optional[str]:
    stakeholder_role: str = ""
    request_store = token_utils.get_request_store(info.context)
    entity = request_store.get("entity")

    if entity == "GROUP":
        stakeholder_role = await group_access_domain.get_stakeholder_role(
            email=parent.email,
            group_name=request_store["group_name"],
            is_registered=parent.is_registered,
        )

    elif entity == "ORGANIZATION":
        stakeholder_role = await orgs_domain.get_stakeholder_role(
            email=parent.email,
            is_registered=parent.is_registered,
            organization_id=request_store["organization_id"],
        )

    return stakeholder_role if stakeholder_role else None
