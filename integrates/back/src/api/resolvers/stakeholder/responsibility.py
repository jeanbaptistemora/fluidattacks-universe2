from dataloaders import (
    Dataloaders,
)
from db_model.group_access.enums import (
    GroupInvitiationState,
)
from db_model.group_access.types import (
    GroupAccess,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from group_access.domain import (
    exists,
)
from newutils import (
    token as token_utils,
)
from newutils.group_access import (
    format_invitation_state,
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
    loaders: Dataloaders = info.context.loaders

    if entity == "GROUP":
        if await exists(loaders, request_store["group_name"], parent.email):
            group_access: GroupAccess = await loaders.group_access.load(
                (request_store["group_name"], parent.email)
            )
            invitation_state = format_invitation_state(
                invitation=group_access.invitation,
                is_registered=parent.is_registered,
            )
            return (
                group_access.invitation.responsibility
                if group_access.invitation
                and invitation_state == GroupInvitiationState.PENDING
                else group_access.responsibility
            )

        return None

    return None
