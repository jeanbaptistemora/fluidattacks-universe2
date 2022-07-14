from db_model.stakeholders.types import (
    Stakeholder,
)
from dynamodb.types import (
    Item,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from group_access import (
    domain as group_access_domain,
)
from newutils import (
    stakeholders as stakeholders_utils,
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
    request_store = token_utils.get_request_store(info.context)
    entity = request_store.get("entity")

    if entity == "GROUP":
        group_name: str = request_store["group_name"]
        group_access = await group_access_domain.get_user_access(
            parent.email, group_name
        )
        invitation: Item = group_access.get("invitation", {})
        invitation_state: str = stakeholders_utils.get_invitation_state(
            invitation, parent
        )

    elif entity == "ORGANIZATION":
        organization_id: str = request_store["organization_id"]
        organization_access = await orgs_domain.get_user_access(
            organization_id, parent.email
        )
        invitation = organization_access.get("invitation", {})
        invitation_state = stakeholders_utils.get_invitation_state(
            invitation, parent
        )

    return invitation_state if invitation_state else None
