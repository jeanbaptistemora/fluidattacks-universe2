import authz
from dataloaders import (
    Dataloaders,
)
from db_model.group_access.types import (
    GroupAccess,
)
from db_model.organization_access.enums import (
    InvitiationState,
)
from db_model.organization_access.types import (
    OrganizationAccess,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    token as token_utils,
)
from newutils.group_access import (
    format_group_invitation_state,
)
from newutils.organization_access import (
    format_org_invitation_state,
)
from typing import (
    Optional,
)


async def resolve(
    parent: Stakeholder,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Optional[str]:
    loaders: Dataloaders = info.context.loaders
    stakeholder_role: Optional[str] = ""
    request_store = token_utils.get_request_store(info.context)
    entity = request_store.get("entity")

    if entity == "GROUP":
        group_name = request_store["group_name"]
        group_access: GroupAccess = await loaders.group_access.load(
            (group_name, parent.email)
        )
        invitation_state = format_group_invitation_state(
            invitation=group_access.invitation,
            is_registered=parent.is_registered,
        )
        if (
            group_access.invitation
            and invitation_state == InvitiationState.PENDING
        ):
            stakeholder_role = group_access.invitation.role
        else:
            stakeholder_role = await authz.get_group_level_role(
                parent.email, group_name
            )

    elif entity == "ORGANIZATION":
        organization_id = request_store["organization_id"]
        org_access: OrganizationAccess = (
            await loaders.organization_access.load(
                (organization_id, parent.email)
            )
        )
        invitation_state = format_org_invitation_state(
            invitation=org_access.invitation,
            is_registered=parent.is_registered,
        )
        if (
            org_access.invitation
            and invitation_state == InvitiationState.PENDING
        ):
            stakeholder_role = org_access.invitation.role
        else:
            stakeholder_role = await authz.get_organization_level_role(
                parent.email, organization_id
            )

    return stakeholder_role if stakeholder_role else None
