from .schema import (
    STAKEHOLDER,
)
import authz
from dataloaders import (
    Dataloaders,
)
from db_model.group_access.enums import (
    GroupInvitiationState,
)
from db_model.group_access.types import (
    GroupAccess,
    GroupAccessRequest,
    GroupAccessState,
)
from db_model.organization_access.enums import (
    OrganizationInvitiationState,
)
from db_model.organization_access.types import (
    OrganizationAccessRequest,
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
    datetime as datetime_utils,
)
from newutils.group_access import (
    format_invitation_state as format_group_invitation_state,
)
from newutils.organization_access import (
    format_invitation_state as format_org_invitation_state,
)
from sessions import (
    domain as sessions_domain,
)
from typing import (
    Optional,
)


@STAKEHOLDER.field("role")
async def resolve(
    parent: Stakeholder,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> Optional[str]:
    loaders: Dataloaders = info.context.loaders
    stakeholder_role: str = ""
    request_store = sessions_domain.get_request_store(info.context)
    entity = request_store.get("entity")

    if entity == "GROUP":
        group_name = request_store["group_name"]
        if not await exists(loaders, group_name, parent.email):
            group_access = GroupAccess(
                email=parent.email,
                group_name=group_name,
                state=GroupAccessState(
                    modified_date=datetime_utils.get_utc_now()
                ),
            )
        else:
            group_access = await loaders.group_access.load(
                GroupAccessRequest(group_name=group_name, email=parent.email)
            )
        group_invitation_state = format_group_invitation_state(
            invitation=group_access.invitation,
            is_registered=parent.is_registered,
        )
        stakeholder_role = (
            group_access.invitation.role
            if group_access.invitation
            and group_invitation_state == GroupInvitiationState.PENDING
            else await authz.get_group_level_role(
                loaders, parent.email, group_name
            )
        )

    elif entity == "ORGANIZATION":
        organization_id = request_store["organization_id"]
        if organization_access := await loaders.organization_access.load(
            OrganizationAccessRequest(
                organization_id=organization_id, email=parent.email
            )
        ):
            org_invitation_state = format_org_invitation_state(
                invitation=organization_access.invitation,
                is_registered=parent.is_registered,
            )
            stakeholder_role = (
                organization_access.invitation.role
                if organization_access.invitation
                and org_invitation_state
                == OrganizationInvitiationState.PENDING
                else await authz.get_organization_level_role(
                    loaders, parent.email, organization_id
                )
            )

    return stakeholder_role if stakeholder_role else None
